/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81.h
Label Definition File: CWE121_Stack_Based_Buffer_Overflow__CWE193.label.xml
Template File: sources-sink-81.tmpl.h
*/
/*
 * @description
 * CWE: 121 Stack Based Buffer Overflow
 * BadSource:  Point data to a buffer that does not have space for a NULL terminator
 * GoodSource: Point data to a buffer that includes space for a NULL terminator
 * Sinks: loop
 *    BadSink : Copy array to data using a loop
 * Flow Variant: 81 Data flow: data passed in a parameter to an virtual method called via a reference
 *
 * */

#include "std_testcase.h"

#ifndef _WIN32
#include <wchar.h>
#endif

/* MAINTENANCE NOTE: The length of this string should equal the 10 */
#define SRC_STRING L"AAAAAAAAAA"

namespace CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81
{

class CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81_base
{
public:
    /* pure virtual function */
    virtual void action(wchar_t * data) const = 0;
};

#ifndef OMITBAD

class CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81_bad : public CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81_base
{
public:
    void action(wchar_t * data) const;
};

#endif /* OMITBAD */

#ifndef OMITGOOD

class CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81_goodG2B : public CWE121_Stack_Based_Buffer_Overflow__CWE193_wchar_t_declare_loop_81_base
{
public:
    void action(wchar_t * data) const;
};

#endif /* OMITGOOD */

}
