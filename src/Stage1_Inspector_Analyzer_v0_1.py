#!/usr/bin/env python3
import argparse
import collections
import statistics
import struct
import sys
from pathlib import Path

FILE_HEADER = struct.Struct('<8sHHIQII')
RECORD_HEADER = struct.Struct('<4sIQIIIHBBHHHHIBBBBBBBBBBH8s')
# Record header fields correspond exactly to the 64-byte Stage 1 v1 layout.
assert FILE_HEADER.size == 32
assert RECORD_HEADER.size == 64
MB_BYTES = 8

PIC = {1:'I', 2:'P', 3:'B', 4:'D'}
STRUCT = {1:'TOP_FIELD', 2:'BOTTOM_FIELD', 3:'FRAME'}
TRANSFORM = {0:'NONE', 1:'FRAME', 2:'FIELD'}
CODING = {1:'SKIPPED', 2:'INTRA', 3:'INTER'}
MOTION_SOURCE = {0:'NONE', 1:'CODED', 2:'DERIVED', 3:'INHERITED'}

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('; '.join(errors[:10]))

def pct(n, d):
    return 0.0 if not d else 100.0*n/d

def unpack_mb(raw):
    t,c,q,qu,cbp,mtype,dirs,packed = raw
    return {
        'transform':t,
        'coding':c,
        'q':q,
        'q_update':qu,
        'cbp':cbp,
        'motion_type_raw':mtype,
        'motion_dir_bits':dirs,
        'motion_source':packed & 0x03,
        'valid':bool(packed & 0x04),
        'q_inherited':bool(packed & 0x08),
        'pred_derived':bool(packed & 0x10),
        'dct_read':bool(packed & 0x20),
        'reserved':packed & 0xC0,
        'packed':packed,
    }

def validate_mb(mb, rec, idx, errors):
    prefix=f"record {rec['output_ordinal']} MB {idx}"
    if mb['transform'] not in (0,1,2): errors.append(f'{prefix}: invalid transform {mb["transform"]}')
    if mb['coding'] not in (1,2,3): errors.append(f'{prefix}: invalid coding {mb["coding"]}')
    if mb['q_update'] not in (0,1): errors.append(f'{prefix}: invalid q_update {mb["q_update"]}')
    if mb['cbp'] > 63: errors.append(f'{prefix}: CBP {mb["cbp"]} exceeds 4:2:0 range')
    if mb['motion_type_raw'] > 3: errors.append(f'{prefix}: motion_type_raw {mb["motion_type_raw"]} > 3')
    if mb['motion_dir_bits'] & ~3: errors.append(f'{prefix}: invalid motion_dir_bits {mb["motion_dir_bits"]}')
    if mb['reserved']: errors.append(f'{prefix}: reserved packed bits set 0x{mb["reserved"]:02x}')
    if not mb['valid']: errors.append(f'{prefix}: macroblock not marked valid')
    if mb['q_inherited'] != (mb['q_update'] == 0):
        errors.append(f'{prefix}: q_inherited duplicate flag mismatch')
    if mb['pred_derived'] != (mb['motion_source'] in (2,3)):
        errors.append(f'{prefix}: pred_derived duplicate flag mismatch')
    if mb['coding'] == 1:
        if mb['transform'] != 0: errors.append(f'{prefix}: SKIPPED is not NONE')
        if mb['q_update'] != 0: errors.append(f'{prefix}: SKIPPED has q_update')
        if mb['dct_read']: errors.append(f'{prefix}: SKIPPED has dct_read')
        if mb['motion_source'] == 1: errors.append(f'{prefix}: SKIPPED has CODED motion source')
    if mb['motion_source'] == 3:
        if not (mb['coding'] == 1 and rec['picture_coding_type'] == 3):
            errors.append(f'{prefix}: INHERITED motion outside skipped B picture')
    if mb['motion_source'] == 0 and mb['motion_dir_bits'] != 0:
        errors.append(f'{prefix}: motion dirs nonzero with no motion source')
    if mb['dct_read']:
        if rec['picture_structure'] != 3 or rec['frame_pred_frame_dct'] != 0 or mb['coding'] == 1:
            errors.append(f'{prefix}: dct_read outside allowed context')
    if mb['transform'] == 2:
        if not mb['dct_read'] or rec['picture_structure'] != 3 or rec['frame_pred_frame_dct'] != 0 or mb['coding'] == 1:
            errors.append(f'{prefix}: FIELD without valid dct_type context')
    if mb['coding'] == 3 and mb['cbp'] == 0 and mb['transform'] != 0:
        errors.append(f'{prefix}: INTER CBP=0 is not NONE')

def load_index(path):
    errors=[]
    records=[]
    path=Path(path)
    with path.open('rb') as f:
        raw=f.read(FILE_HEADER.size)
        if len(raw)!=FILE_HEADER.size:
            raise ValidationError(['truncated file header'])
        magic, version, hsize, endian, final_count, file_flags, reserved = FILE_HEADER.unpack(raw)
        if magic != b'S1MBIDX1': errors.append(f'bad file magic {magic!r}')
        if version != 1: errors.append(f'unsupported version {version}')
        if hsize != 32: errors.append(f'file_header_size {hsize} != 32')
        if endian != 0x01020304: errors.append(f'bad endian marker 0x{endian:08x}')
        if reserved != 0: errors.append('file header reserved field is nonzero')
        if not (file_flags & 1): errors.append('file is not marked complete')
        if file_flags & ~1: errors.append(f'file has unsupported/error flags 0x{file_flags & ~1:08x}')
        expected_ordinal=0
        while True:
            pos=f.tell()
            rh=f.read(RECORD_HEADER.size)
            if not rh: break
            if len(rh)!=RECORD_HEADER.size:
                errors.append(f'truncated record header at offset {pos}')
                break
            vals=RECORD_HEADER.unpack(rh)
            (rmagic,rsize,ordinal,seq_ord,bit_fn,seq_fn,temp_ref,pictype,picstruct,
             cwidth,cheight,mbw,mbh,mbcount,prog,tff,rff,fpfd,qstype,chroma,
             cintra,cnonintra,cdiffi,cdiffn,rflags,rreserved)=vals
            rec={
                'record_offset':pos,'record_size':rsize,'output_ordinal':ordinal,
                'sequence_ordinal':seq_ord,'source_bitstream_framenum':bit_fn,
                'source_sequence_framenum':seq_fn,'temporal_reference':temp_ref,
                'picture_coding_type':pictype,'picture_structure':picstruct,
                'coded_width':cwidth,'coded_height':cheight,'mb_width':mbw,'mb_height':mbh,
                'mb_count':mbcount,'progressive_frame':prog,'top_field_first':tff,
                'repeat_first_field':rff,'frame_pred_frame_dct':fpfd,'q_scale_type':qstype,
                'chroma_format':chroma,'custom_intra':cintra,'custom_non_intra':cnonintra,
                'chroma_intra_diff':cdiffi,'chroma_non_intra_diff':cdiffn,'record_flags':rflags,
            }
            if rmagic != b'FRM1': errors.append(f'record {ordinal}: bad magic {rmagic!r}')
            if ordinal != expected_ordinal: errors.append(f'record ordinal {ordinal} expected {expected_ordinal}')
            expected_ordinal += 1
            if mbcount != mbw*mbh: errors.append(f'record {ordinal}: mb_count mismatch')
            expected_size=64+mbcount*MB_BYTES
            if rsize != expected_size: errors.append(f'record {ordinal}: record_size {rsize} != {expected_size}')
            if rreserved != b'\x00'*8: errors.append(f'record {ordinal}: reserved bytes nonzero')
            if rflags != 0x0007: errors.append(f'record {ordinal}: record_flags 0x{rflags:04x} != 0x0007')
            payload=f.read(mbcount*MB_BYTES)
            if len(payload)!=mbcount*MB_BYTES:
                errors.append(f'record {ordinal}: truncated MB payload')
                break
            mbs=[]
            for i in range(mbcount):
                mb=unpack_mb(payload[i*8:(i+1)*8])
                validate_mb(mb,rec,i,errors)
                mbs.append(mb)
            rec['mbs']=mbs
            records.append(rec)
        if len(records) != final_count:
            errors.append(f'parsed record count {len(records)} != header final_record_count {final_count}')
    if errors:
        raise ValidationError(errors)
    return {'path':str(path),'version':version,'file_flags':file_flags,'records':records}

def counter_text(counter, total=None):
    parts=[]
    for k,v in sorted(counter.items(), key=lambda kv: str(kv[0])):
        if total is None: parts.append(f'{k}={v}')
        else: parts.append(f'{k}={v} ({pct(v,total):.2f}%)')
    return ', '.join(parts)

def summary_data(index):
    recs=index['records']; allmb=[mb for r in recs for mb in r['mbs']]
    ptypes=collections.Counter(PIC.get(r['picture_coding_type'],str(r['picture_coding_type'])) for r in recs)
    structs=collections.Counter(STRUCT.get(r['picture_structure'],str(r['picture_structure'])) for r in recs)
    transforms=collections.Counter(TRANSFORM[mb['transform']] for mb in allmb)
    coding=collections.Counter(CODING[mb['coding']] for mb in allmb)
    q= [mb['q'] for mb in allmb]
    mixed=0
    state_by_pic={p:collections.Counter() for p in ('I','P','B','D')}
    coding_by_pic={p:collections.Counter() for p in ('I','P','B','D')}
    neigh_h=collections.Counter(); neigh_v=collections.Counter()
    q_by_pic={p:[] for p in ('I','P','B','D')}
    for r in recs:
        p=PIC.get(r['picture_coding_type'],str(r['picture_coding_type']))
        states=set(mb['transform'] for mb in r['mbs'])
        if 1 in states and 2 in states: mixed+=1
        for mb in r['mbs']:
            if p in state_by_pic:
                state_by_pic[p][TRANSFORM[mb['transform']]]+=1
                coding_by_pic[p][CODING[mb['coding']]]+=1
                q_by_pic[p].append(mb['q'])
        w=r['mb_width']; h=r['mb_height']; m=r['mbs']
        for y in range(h):
            for x in range(w):
                i=y*w+x
                if x+1<w:
                    a,b=sorted((TRANSFORM[m[i]['transform']],TRANSFORM[m[i+1]['transform']]))
                    neigh_h[f'{a}-{b}']+=1
                if y+1<h:
                    a,b=sorted((TRANSFORM[m[i]['transform']],TRANSFORM[m[i+w]['transform']]))
                    neigh_v[f'{a}-{b}']+=1
    return {
        'record_count':len(recs),'sequence_count':len(set(r['sequence_ordinal'] for r in recs)),
        'picture_types':ptypes,'structures':structs,'transforms':transforms,'coding':coding,
        'q':q,'mixed_frame_field_frames':mixed,'state_by_pic':state_by_pic,'coding_by_pic':coding_by_pic,
        'q_by_pic':q_by_pic,'neigh_h':neigh_h,'neigh_v':neigh_v,
        'custom_intra_frames':sum(r['custom_intra'] for r in recs),
        'custom_non_intra_frames':sum(r['custom_non_intra'] for r in recs),
        'chroma_intra_diff_frames':sum(r['chroma_intra_diff'] for r in recs),
        'chroma_non_intra_diff_frames':sum(r['chroma_non_intra_diff'] for r in recs),
        'q_updates':sum(mb['q_update'] for mb in allmb),
        'dct_read_count':sum(mb['dct_read'] for mb in allmb),
        'inter_cbp0_dctread':sum(1 for mb in allmb if mb['coding']==3 and mb['cbp']==0 and mb['dct_read']),
    }

def print_summary(index, expected=None):
    s=summary_data(index); recs=index['records']; total_mb=sum(r['mb_count'] for r in recs)
    print(f"VALID: {index['path']}")
    print(f"records={s['record_count']} sequences={s['sequence_count']}")
    if expected is not None:
        status='PASS' if s['record_count']==expected else 'FAIL'
        print(f"expected_frames={expected} count_gate={status}")
    dims=collections.Counter((r['coded_width'],r['coded_height'],r['mb_width'],r['mb_height']) for r in recs)
    print('dimensions:', ', '.join(f'{k[0]}x{k[1]} MB={k[2]}x{k[3]} frames={v}' for k,v in dims.items()))
    print('picture types:', counter_text(s['picture_types'],s['record_count']))
    print('picture structures:', counter_text(s['structures'],s['record_count']))
    print('transform states:', counter_text(s['transforms'],total_mb))
    print('coding states:', counter_text(s['coding'],total_mb))
    print(f"mixed FRAME/FIELD frames={s['mixed_frame_field_frames']} ({pct(s['mixed_frame_field_frames'],s['record_count']):.2f}%)")
    if s['q']:
        print(f"QP effective: min={min(s['q'])} max={max(s['q'])} mean={statistics.fmean(s['q']):.3f} median={statistics.median(s['q'])}")
    print(f"macroblock Q updates={s['q_updates']} ({pct(s['q_updates'],total_mb):.2f}%)")
    print(f"dct_type bits read={s['dct_read_count']} ({pct(s['dct_read_count'],total_mb):.2f}%)")
    print(f"INTER CBP=0 with dct_type bit actually read={s['inter_cbp0_dctread']}")
    print(f"custom matrix frames: intra={s['custom_intra_frames']} non_intra={s['custom_non_intra_frames']} chroma_intra_diff={s['chroma_intra_diff_frames']} chroma_non_intra_diff={s['chroma_non_intra_diff_frames']}")
    for p in ('I','P','B'):
        n=sum(s['state_by_pic'][p].values())
        if n:
            print(f"{p} transforms: {counter_text(s['state_by_pic'][p],n)}")
    print('horizontal state neighbours:', counter_text(s['neigh_h']))
    print('vertical state neighbours:', counter_text(s['neigh_v']))
    qhist=collections.Counter(s['q'])
    print('QP histogram:', counter_text(qhist))

def print_frame(index,n):
    r=index['records'][n]
    print(f"frame {n}: type={PIC.get(r['picture_coding_type'],r['picture_coding_type'])} structure={STRUCT.get(r['picture_structure'],r['picture_structure'])} temporal_reference={r['temporal_reference']}")
    print(f"  seq={r['sequence_ordinal']} source_bitstream={r['source_bitstream_framenum']} source_sequence={r['source_sequence_framenum']}")
    print(f"  coded={r['coded_width']}x{r['coded_height']} MB={r['mb_width']}x{r['mb_height']} progressive={r['progressive_frame']} top_first={r['top_field_first']} repeat_first={r['repeat_first_field']} frame_pred_frame_dct={r['frame_pred_frame_dct']} q_scale_type={r['q_scale_type']}")
    c=collections.Counter(TRANSFORM[mb['transform']] for mb in r['mbs'])
    q=[mb['q'] for mb in r['mbs']]
    print('  transforms:', counter_text(c,len(r['mbs'])))
    print(f"  QP: min={min(q)} max={max(q)} mean={statistics.fmean(q):.3f} median={statistics.median(q)}")

def print_mb(index,n,x,y):
    r=index['records'][n]
    if not (0<=x<r['mb_width'] and 0<=y<r['mb_height']): raise SystemExit('MB coordinate out of range')
    mb=r['mbs'][y*r['mb_width']+x]
    print(f"frame={n} x={x} y={y}")
    for k,v in mb.items():
        if k=='transform': v=f'{v} ({TRANSFORM.get(v)})'
        elif k=='coding': v=f'{v} ({CODING.get(v)})'
        elif k=='motion_source': v=f'{v} ({MOTION_SOURCE.get(v)})'
        print(f'{k}={v}')

def dump_frame(index,n):
    r=index['records'][n]; chars={0:'.',1:'F',2:'D'}
    print('legend: F=FRAME D=FIELD .=NONE')
    for y in range(r['mb_height']):
        print(''.join(chars[mb['transform']] for mb in r['mbs'][y*r['mb_width']:(y+1)*r['mb_width']]))

def compare(a,b):
    sa,sb=summary_data(a),summary_data(b)
    print(f"A: {a['path']}")
    print(f"B: {b['path']}")
    print(f"records: A={sa['record_count']} B={sb['record_count']}")
    for label,key in [('transforms','transforms'),('coding','coding')]:
        print(label+':')
        keys=sorted(set(sa[key])|set(sb[key]))
        for k in keys: print(f'  {k}: A={sa[key][k]} B={sb[key][k]}')
    for label,s in [('A',sa),('B',sb)]:
        q=s['q']; print(f"{label} QP min={min(q)} max={max(q)} mean={statistics.fmean(q):.3f} median={statistics.median(q)}")
    print(f"mixed FRAME/FIELD frames: A={sa['mixed_frame_field_frames']} B={sb['mixed_frame_field_frames']}")
    print(f"custom intra frames: A={sa['custom_intra_frames']} B={sb['custom_intra_frames']}")
    print(f"custom non-intra frames: A={sa['custom_non_intra_frames']} B={sb['custom_non_intra_frames']}")

def main():
    p=argparse.ArgumentParser(description='Stage 1 MPEG-2 inspector temporary-index analyzer')
    sub=p.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('summary'); s.add_argument('index'); s.add_argument('--expected-frames',type=int)
    f=sub.add_parser('frame'); f.add_argument('index'); f.add_argument('n',type=int)
    m=sub.add_parser('mb'); m.add_argument('index'); m.add_argument('n',type=int); m.add_argument('x',type=int); m.add_argument('y',type=int)
    d=sub.add_parser('dump-frame'); d.add_argument('index'); d.add_argument('n',type=int)
    c=sub.add_parser('compare'); c.add_argument('index_a'); c.add_argument('index_b')
    args=p.parse_args()
    try:
        if args.cmd=='compare':
            a=load_index(args.index_a); b=load_index(args.index_b); compare(a,b)
        else:
            idx=load_index(args.index)
            if args.cmd=='summary': print_summary(idx,args.expected_frames)
            elif args.cmd=='frame': print_frame(idx,args.n)
            elif args.cmd=='mb': print_mb(idx,args.n,args.x,args.y)
            elif args.cmd=='dump-frame': dump_frame(idx,args.n)
    except ValidationError as e:
        print('INVALID Stage 1 index',file=sys.stderr)
        for err in e.errors[:100]: print('  '+err,file=sys.stderr)
        if len(e.errors)>100: print(f'  ... {len(e.errors)-100} more errors',file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())
