/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE122_Heap_Based_Buffer_Overflow__CWE135_81.h
Label Definition File: CWE122_Heap_Based_Buffer_Overflow__CWE135.label.xml
Template File: sources-sinks-81.tmpl.h
*/
/*
 * @description
 * CWE: 122 Heap Based Buffer Overflow
 * BadSource:  Void pointer to a wchar_t array
 * GoodSource: Void pointer to a char array
 * Sinks:
 *    GoodSink: Allocate memory using wcslen() and copy data
 *    BadSink : Allocate memory using strlen() and copy data
 * Flow Variant: 81 Data flow: data passed in a parameter to an virtual method called via a reference
 *
 * */

#include "std_testcase.h"

#include <wchar.h>

namespace CWE122_Heap_Based_Buffer_Overflow__CWE135_81
{

class CWE122_Heap_Based_Buffer_Overflow__CWE135_81_base
{
public:
    /* pure virtual function */
    virtual void action(void * data) const = 0;
};

#ifndef OMITBAD

class CWE122_Heap_Based_Buffer_Overflow__CWE135_81_bad : public CWE122_Heap_Based_Buffer_Overflow__CWE135_81_base
{
public:
    void action(void * data) const;
};

#endif /* OMITBAD */

#ifndef OMITGOOD

class CWE122_Heap_Based_Buffer_Overflow__CWE135_81_goodG2B : public CWE122_Heap_Based_Buffer_Overflow__CWE135_81_base
{
public:
    void action(void * data) const;
};

class CWE122_Heap_Based_Buffer_Overflow__CWE135_81_goodB2G : public CWE122_Heap_Based_Buffer_Overflow__CWE135_81_base
{
public:
    void action(void * data) const;
};

#endif /* OMITGOOD */

}
