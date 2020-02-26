/* config.h.  Generated from config.h.in by configure.  */
/* config.h.in.  Generated from configure.ac by autoheader.  */

/* Define to 1 if the LAPACK package is available */
#define COIN_HAS_LAPACK 1

/* Define to 1 if Metis is available. */
#define COIN_HAS_METIS 1

/* Define to a macro mangling the given C identifier (in lower and upper
   case). */
#define COIN_LAPACK_FUNC(name,NAME) name ## _

/* As COIN_LAPACK_FUNC, but for C identifiers containing underscores. */
#define COIN_LAPACK_FUNC_(name,NAME) name ## _

/* Define to dummy `main' function (if any) required to link to the Fortran
   libraries. */
/* #undef FC_DUMMY_MAIN */

/* Define if F77 and FC dummy `main' functions are identical. */
/* #undef FC_DUMMY_MAIN_EQ_F77 */

/* Define to a macro mangling the given C identifier (in lower and upper
   case), which must not contain underscores, for linking with Fortran. */
#define FC_FUNC(name,NAME) name ## _

/* As FC_FUNC, but for C identifiers containing underscores. */
#define FC_FUNC_(name,NAME) name ## _

/* Define to 1 if your Fortran compiler doesn't accept -c and -o together. */
/* #undef FC_NO_MINUS_C_MINUS_O */

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#define LT_OBJDIR ".libs/"

/* Library Visibility Attribute */
#define MUMPS_CALL 

/* Library Visibility Attribute */
#define MUMPS_EXPORT 

/* Version number of project */
#define MUMPS_VERSION "2.0.0"

/* Major version number of project. */
#define MUMPS_VERSION_MAJOR 2

/* Minor version number of project. */
#define MUMPS_VERSION_MINOR 0

/* Release version number of project. */
#define MUMPS_VERSION_RELEASE 0

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "https://github.com/coin-or-tools/ThirdParty-Mumps/issues/new"

/* Define to the full name of this package. */
#define PACKAGE_NAME "ThirdPartyMumps"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "ThirdPartyMumps 2.0.0"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "thirdpartymumps"

/* Define to the home page for this package. */
#define PACKAGE_URL "https://github.com/coin-or-tools/ThirdParty-Mumps"

/* Define to the version of this package. */
#define PACKAGE_VERSION "2.0.0"

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1
