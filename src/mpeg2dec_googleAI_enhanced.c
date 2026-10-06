/* mpeg2dec.c, main(), initialization, option processing                    */

/* Copyright (C) 1996, MPEG Software Simulation Group. All Rights Reserved. */

/*
 * Disclaimer of Warranty
 *
 * These software programs are available to the user without any license fee or
 * royalty on an "as is" basis.  The MPEG Software Simulation Group disclaims
 * any and all warranties, whether express, implied, or statuary, including any
 * implied warranties or merchantability or of fitness for a particular
 * purpose.  In no event shall the copyright-holder be liable for any
 * incidental, punitive, or consequential damages of any kind whatsoever
 * arising from the use of these programs.
 *
 * This disclaimer of warranty extends to the user of these programs and user's
 * customers, employees, agents, transferees, successors, and assigns.
 *
 * The MPEG Software Simulation Group does not represent or warrant that the
 * programs furnished hereunder are free of infringement of any third-party
 * patents.
 *
 * Commercial implementations of MPEG-1 and MPEG-2 video, including shareware,
 * are subject to royalty fees to patent holders.  Many of these patents are
 * general enough such that they are unavoidable regardless of implementation
 * design.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <fcntl.h>
#include <string.h>

#ifdef _WIN32
#include <io.h>
#include <fcntl.h>
#endif

#define GLOBAL
#include "config.h"
#include "global.h"

/* Custom Global: Target .idx2 index filename */
char *Index_Filename = "output.idx2";

/* private prototypes */
static int  video_sequence _ANSI_ARGS_((int *framenum));
static int Decode_Bitstream _ANSI_ARGS_((void));
static int  Headers _ANSI_ARGS_((void));
static void Initialize_Sequence _ANSI_ARGS_((void));
static void Initialize_Decoder _ANSI_ARGS_((void));
static void Deinitialize_Sequence _ANSI_ARGS_((void));
static void Process_Options _ANSI_ARGS_((int argc, char *argv[]));


#if OLD
static int  Get_Val _ANSI_ARGS_((char *argv[]));
#endif

/* #define DEBUG */

static void Clear_Options();
#ifdef DEBUG
static void Print_Options();
#endif

int main(argc,argv)
int argc;
char *argv[];
{
  int ret, code;

  Clear_Options();

  /* decode command line arguments */
  Process_Options(argc,argv);

#ifdef DEBUG
  Print_Options();
#endif

  ld = &base; /* select base layer context */

  /* open MPEG base layer bitstream file(s) */
  /* NOTE: this is either a base layer stream or a spatial enhancement stream */
  if (strcmp(Main_Bitstream_Filename, "-") == 0)
  {
#ifdef _WIN32
    _setmode(_fileno(stdin), _O_BINARY);
#endif
    base.Infile = _fileno(stdin);
  }
  else if ((base.Infile=open(Main_Bitstream_Filename,O_RDONLY|O_BINARY))<0)
  {
    fprintf(stderr,"Base layer input file %s not found\n", Main_Bitstream_Filename);
    exit(1);
  }

  /* if reading from standard input pipe, skip non-seekable header detection */
  if (strcmp(Main_Bitstream_Filename, "-") == 0)
  {
    Initialize_Buffer();
  }
  else
  {
    if(base.Infile != 0)
    {
      Initialize_Buffer(); 
    
      if(Show_Bits(8)==0x47)
      {
        sprintf(Error_Text,"Decoder currently does not parse transport streams\n");
        Error(Error_Text);
      }

      next_start_code();
      code = Show_Bits(32);

      switch(code)
      {
      case SEQUENCE_HEADER_CODE:
        break;
      case PACK_START_CODE:
        System_Stream_Flag = 1;
      case VIDEO_ELEMENTARY_STREAM:
        System_Stream_Flag = 1;
        break;
      default:
        sprintf(Error_Text,"Unable to recognize stream type\n");
        Error(Error_Text);
        break;
      }

      lseek(base.Infile, 0l, 0);
      Initialize_Buffer(); 
    }

    if(base.Infile!=0)
    {
      lseek(base.Infile, 0l, 0);
    }

    Initialize_Buffer(); 
  }

  if(Two_Streams)
  {
    ld = &enhan; /* select enhancement layer context */

    if ((enhan.Infile = open(Enhancement_Layer_Bitstream_Filename,O_RDONLY|O_BINARY))<0)
    {
      sprintf(Error_Text,"enhancment layer bitstream file %s not found\n",
        Enhancement_Layer_Bitstream_Filename);

      Error(Error_Text);
    }

    Initialize_Buffer();
    ld = &base;
  }

  Initialize_Decoder();

  ret = Decode_Bitstream();

  if (base.Infile != _fileno(stdin))
    close(base.Infile);

  if (Two_Streams)
    close(enhan.Infile);

  return 0;
}

/* IMPLEMENTAION specific rouintes */
static void Initialize_Decoder()
{
  int i;

  /* Clip table */
  if (!(Clip=(unsigned char *)malloc(1024)))
    Error("Clip[] malloc failed\n");

  Clip += 384;

  for (i=-384; i<640; i++)
    Clip[i] = (i<0) ? 0 : ((i>255) ? 255 : i);

  /* IDCT */
  if (Reference_IDCT_Flag)
    Initialize_Reference_IDCT();
  else
    Initialize_Fast_IDCT();

}

/* mostly IMPLEMENTAION specific rouintes */
static void Initialize_Sequence()
{
  int cc, size;
  static int Table_6_20[3] = {6,8,12};

  /* check scalability mode of enhancement layer */
  if (Two_Streams && (enhan.scalable_mode!=SC_SNR) && (base.scalable_mode!=SC_DP))
    Error("unsupported scalability mode\n");

  /* force MPEG-1 parameters for proper decoder behavior */
  /* see ISO/IEC 13818-2 section D.9.14 */
  if (!base.MPEG2_Flag)
  {
    progressive_sequence = 1;
    progressive_frame = 1;
    picture_structure = FRAME_PICTURE;
    frame_pred_frame_dct = 1;
    chroma_format = CHROMA420;
    matrix_coefficients = 5;
  }

  /* round to nearest multiple of coded macroblocks */
  /* ISO/IEC 13818-2 section 6.3.3 sequence_header() */
  mb_width = (horizontal_size+15)/16;
  mb_height = (base.MPEG2_Flag && !progressive_sequence) ? 2*((vertical_size+31)/32)
                                        : (vertical_size+15)/16;

  Coded_Picture_Width = 16*mb_width;
  Coded_Picture_Height = 16*mb_height;

  /* ISO/IEC 13818-2 sections 6.1.1.8, 6.1.1.9, and 6.1.1.10 */
  Chroma_Width = (chroma_format==CHROMA444) ? Coded_Picture_Width
                                           : Coded_Picture_Width>>1;
  Chroma_Height = (chroma_format!=CHROMA420) ? Coded_Picture_Height
                                            : Coded_Picture_Height>>1;
  
  /* derived based on Table 6-20 in ISO/IEC 13818-2 section 6.3.17 */
  block_count = Table_6_20[chroma_format-1];

  for (cc=0; cc<3; cc++)
  {
    if (cc==0)
      size = Coded_Picture_Width*Coded_Picture_Height;
    else
      size = Chroma_Width*Chroma_Height;

    if (!(backward_reference_frame[cc] = (unsigned char *)malloc(size)))
      Error("backward_reference_frame[] malloc failed\n");

    if (!(forward_reference_frame[cc] = (unsigned char *)malloc(size)))
      Error("forward_reference_frame[] malloc failed\n");

    if (!(auxframe[cc] = (unsigned char *)malloc(size)))
      Error("auxframe[] malloc failed\n");

    if(Ersatz_Flag)
      if (!(substitute_frame[cc] = (unsigned char *)malloc(size)))
        Error("substitute_frame[] malloc failed\n");


    if (base.scalable_mode==SC_SPAT)
    {
      /* this assumes lower layer is 4:2:0 */
      if (!(llframe0[cc] = (unsigned char *)malloc((lower_layer_prediction_horizontal_size*lower_layer_prediction_vertical_size)/(cc?4:1))))
        Error("llframe0 malloc failed\n");
      if (!(llframe1[cc] = (unsigned char *)malloc((lower_layer_prediction_horizontal_size*lower_layer_prediction_vertical_size)/(cc?4:1))))
        Error("llframe1 malloc failed\n");
    }
  }

  /* SCALABILITY: Spatial */
  if (base.scalable_mode==SC_SPAT)
  {
    if (!(lltmp = (short *)malloc(lower_layer_prediction_horizontal_size*((lower_layer_prediction_vertical_size*vertical_subsampling_factor_n)/vertical_subsampling_factor_m)*sizeof(short))))
      Error("lltmp malloc failed\n");
  }

#ifdef DISPLAY
  if (Output_Type==T_X11)
  {
    Initialize_Display_Process("");
    Initialize_Dither_Matrix();
  }
#endif /* DISPLAY */

}

void Error(text)
char *text;
{
  fprintf(stderr,text);
  exit(1);
}

/* Trace_Flag output */
void Print_Bits(code,bits,len)
int code,bits,len;
{
  int i;
  for (i=0; i<len; i++)
    printf("%d",(code>>(bits-1-i))&1);
}



/* option processing */
static void Process_Options(argc,argv)
int argc;                  /* argument count  */
char *argv[];              /* argument vector */
{
  int i, LastArg, NextArg;

  /* at least one argument should be present */
  if (argc<2)
  {
    printf("\n%s, %s\n",Version,Author);
    printf("Usage:  mpeg2decode {options}\n\
Options: -b  file  main bitstream (base or spatial enhancement layer)\n\
         -idx file output binary macroblock index file (.idx2)\n\
         -cn file  conformance report (n: level)\n\
         -e  file  enhancement layer bitstream (SNR or Data Partitioning)\n\
         -f        store/display interlaced video in frame format\n\
         -g        concatenated file format for substitution method (-x)\n\
         -in file  information & statistics report  (n: level)\n\
         -l  file  file name pattern for lower layer sequence\n\
                   (for spatial scalability)\n\
         -on file  output format (0:YUV 1:SIF 2:TGA 3:PPM 4:X11 5:X11HiQ)\n\
         -q        disable warnings to stderr\n\
         -r        use double precision reference IDCT\n\
         -t        enable low level tracing to stdout\n\
         -u  file  print user_data to stdio or file\n\
         -vn       verbose output (n: level)\n\
         -x  file  filename pattern of picture substitution sequence\n\n");
    exit(0);
  }


  Output_Type = -1;
  i = 1;

  /* command-line options are proceeded by '-' */

  while(i < argc)
  {
    /* check if this is the last argument */
    LastArg = ((argc-i)==1);

    /* parse ahead to see if another flag immediately follows current argument */
    if(!LastArg)
      NextArg = (argv[i+1][0]=='-' && argv[i+1][1]!='\0');
    else
      NextArg = 0;

    /* Custom Check for -idx <filename> */
    if (strcmp(argv[i], "-idx") == 0)
    {
      if (NextArg || LastArg)
      {
        printf("ERROR: -idx must be followed by output index filename\n");
        exit(ERROR);
      }
      else
      {
        Index_Filename = argv[++i];
      }
    }
    else if(argv[i][0]=='-')
    {
      switch(toupper(argv[i][1]))
      {
      case 'B':
        Main_Bitstream_Flag = 1;

        if(NextArg || LastArg)
        {
          printf("ERROR: -b must be followed the main bitstream filename\n");
        }
        else
          Main_Bitstream_Filename = argv[++i]; 

        break;

      case 'C':
#ifdef VERIFY
        Verify_Flag = atoi(&argv[i][2]); 

        if((Verify_Flag < NO_LAYER) || (Verify_Flag > ALL_LAYERS))
        {
          printf("ERROR: -c level (%d) out of range [%d,%d]\n",
            Verify_Flag, NO_LAYER, ALL_LAYERS);
          exit(ERROR);
        }
#else
        printf("This program not compiled for Verify_Flag option\n");
#endif
        break;

      case 'E':
        Two_Streams = 1;
	                   
        if(NextArg || LastArg)
        {
          printf("ERROR: -e must be followed by filename\n");
          exit(ERROR);
        }
        else
          Enhancement_Layer_Bitstream_Filename = argv[++i]; 

        break;

      case 'F':
        Frame_Store_Flag = 1;
        break;

      case 'G':
        Big_Picture_Flag = 1;
        break;

      case 'I':
#ifdef VERIFY
        Stats_Flag = atoi(&argv[i][2]); 
#else
        printf("WARNING: This program not compiled for -i option\n");
#endif     
        break;
    
      case 'L':
        Spatial_Flag = 1;

       if(NextArg || LastArg)
       {
         printf("ERROR: -l must be followed by filename\n");
         exit(ERROR);
       }
       else
         Lower_Layer_Picture_Filename = argv[++i]; 

        break;

      case 'O':
        Output_Type = atoi(&argv[i][2]); 
  
        if((Output_Type==4) || (Output_Type==5))
          Output_Picture_Filename = "";
        else if(NextArg || LastArg)  
        {
          printf("ERROR: -o must be followed by filename\n");
          exit(ERROR);
        }
        else
          Output_Picture_Filename = argv[++i]; 

#ifdef DISPLAY
        if (Output_Type==T_X11HIQ)
        {
          hiQdither = 1;
          Output_Type=T_X11;
        }
#endif
        break;

      case 'Q':
        Quiet_Flag = 1;
        break;

      case 'R':
        Reference_IDCT_Flag = 1;
        break;
    
      case 'T':
#ifdef TRACE
        Trace_Flag = 1;
#else
        printf("WARNING: This program not compiled for -t option\n");
#endif
        break;

      case 'U':
        User_Data_Flag = 1;

      case 'V':
#ifdef VERBOSE
        Verbose_Flag = atoi(&argv[i][2]); 
#else
        printf("This program not compiled for -v option\n");
#endif
        break;

      case 'X':
        Ersatz_Flag = 1;

       if(NextArg || LastArg)
       {
         printf("ERROR: -x must be followed by filename\n"); 
         exit(ERROR);
       }
       else
        Substitute_Picture_Filename = argv[++i]; 

        break;

      default:
        fprintf(stderr,"undefined option -%c ignored. Exiting program\n", 
          argv[i][1]);
        exit(ERROR);
      }
    }
    
    i++;
  }

  if(Main_Bitstream_Flag!=1)
  {
    printf("There must be a main bitstream specified (-b filename)\n");
  }

  if((Output_Type==4 || Output_Type==5) && Frame_Store_Flag)
    Display_Progressive_Flag = 1;
  else
    Display_Progressive_Flag = 0;

#ifdef VERIFY
    Decode_Layer = ALL_LAYERS;
#endif

  if(Output_Type==-1)
  {
    Output_Type = 9; 
    Output_Picture_Filename = "";
  }

#ifdef DISPLAY
  if (Output_Type==T_X11)
  {
    if(Frame_Store_Flag)
      Display_Progressive_Flag = 1;
    else
      Display_Progressive_Flag = 0;

    Frame_Store_Flag = 1;
  }
#endif
}


#ifdef OLD
static int Get_Val(argv)
char *argv[];
{
  int val;

  if (sscanf(argv[1]+2,"%d",&val)!=1)
    return 0;

  while (isdigit(argv[1][2]))
    argv[1]++;

  return val;
}
#endif

static int Headers()
{
  int ret;
  ld = &base;

  ret = Get_Hdr();

  if (Two_Streams)
  {
    ld = &enhan;
    if (Get_Hdr()!=ret && !Quiet_Flag)
      fprintf(stderr,"streams out of sync\n");
    ld = &base;
  }

  return ret;
}

static int Decode_Bitstream()
{
  int ret;
  int Bitstream_Framenum;

  Bitstream_Framenum = 0;

  for(;;)
  {
#ifdef VERIFY
    Clear_Verify_Headers();
#endif

    ret = Headers();
    
    if(ret==1)
    {
      ret = video_sequence(&Bitstream_Framenum);
    }
    else
      return(ret);
  }
}

static void Deinitialize_Sequence()
{
  int i;
  base.MPEG2_Flag=0;

  for(i=0;i<3;i++)
  {
    free(backward_reference_frame[i]);
    free(forward_reference_frame[i]);
    free(auxframe[i]);

    if (base.scalable_mode==SC_SPAT)
    {
     free(llframe0[i]);
     free(llframe1[i]);
    }
  }

  if (base.scalable_mode==SC_SPAT)
    free(lltmp);

#ifdef DISPLAY
  if (Output_Type==T_X11) 
    Terminate_Display_Process();
#endif
}

static int video_sequence(Bitstream_Framenumber)
int *Bitstream_Framenumber;
{
  int Bitstream_Framenum;
  int Sequence_Framenum;
  int Return_Value;

  Bitstream_Framenum = *Bitstream_Framenumber;
  Sequence_Framenum=0;

  Initialize_Sequence();

  Decode_Picture(Bitstream_Framenum, Sequence_Framenum);

  if (!Second_Field)
  {
    Bitstream_Framenum++;
    Sequence_Framenum++;
  }

  while ((Return_Value=Headers()))
  {
    Decode_Picture(Bitstream_Framenum, Sequence_Framenum);

    if (!Second_Field)
    {
      Bitstream_Framenum++;
      Sequence_Framenum++;
    }
  }

  if (Sequence_Framenum!=0)
  {
    Output_Last_Frame_of_Sequence(Bitstream_Framenum);
  }

  Deinitialize_Sequence();

#ifdef VERIFY
    Clear_Verify_Headers();
#endif

  *Bitstream_Framenumber = Bitstream_Framenum;
  return(Return_Value);
}

static void Clear_Options()
{
  Verbose_Flag = 0;
  Output_Type = 0;
  Output_Picture_Filename = " ";
  hiQdither  = 0;
  Output_Type = 0;
  Frame_Store_Flag = 0;
  Spatial_Flag = 0;
  Lower_Layer_Picture_Filename = " ";
  Reference_IDCT_Flag = 0;
  Trace_Flag = 0;
  Quiet_Flag = 0;
  Ersatz_Flag = 0;
  Substitute_Picture_Filename  = " ";
  Two_Streams = 0;
  Enhancement_Layer_Bitstream_Filename = " ";
  Big_Picture_Flag = 0;
  Main_Bitstream_Flag = 0;
  Main_Bitstream_Filename = " ";
  Verify_Flag = 0;
  Stats_Flag  = 0;
  User_Data_Flag = 0; 
}

#ifdef DEBUG
static void Print_Options()
{
  printf("Verbose_Flag                         = %d\n", Verbose_Flag);
  printf("Output_Type                          = %d\n", Output_Type);
  printf("Output_Picture_Filename              = %s\n", Output_Picture_Filename);
  printf("hiQdither                            = %d\n", hiQdither);
  printf("Output_Type                          = %d\n", Output_Type);
  printf("Frame_Store_Flag                     = %d\n", Frame_Store_Flag);
  printf("Spatial_Flag                         = %d\n", Spatial_Flag);
  printf("Lower_Layer_Picture_Filename         = %s\n", Lower_Layer_Picture_Filename);
  printf("Reference_IDCT_Flag                  = %d\n", Reference_IDCT_Flag);
  printf("Trace_Flag                           = %d\n", Trace_Flag);
  printf("Quiet_Flag                           = %d\n", Quiet_Flag);
  printf("Ersatz_Flag                          = %d\n", Ersatz_Flag);
  printf("Substitute_Picture_Filename          = %s\n", Substitute_Picture_Filename);
  printf("Two_Streams                          = %d\n", Two_Streams);
  printf("Enhancement_Layer_Bitstream_Filename = %s\n", Enhancement_Layer_Bitstream_Filename);
  printf("Big_Picture_Flag                     = %d\n", Big_Picture_Flag);
  printf("Main_Bitstream_Flag                  = %d\n", Main_Bitstream_Flag);
  printf("Main_Bitstream_Filename              = %s\n", Main_Bitstream_Filename);
  printf("Verify_Flag                          = %d\n", Verify_Flag);
  printf("Stats_Flag                           = %d\n", Stats_Flag);
  printf("User_Data_Flag                       = %d\n", User_Data_Flag);
}
#endif
