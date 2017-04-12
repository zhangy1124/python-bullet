#ifndef __PYTHONREADING_OBJECT_H_
#define __PYTHONREADING_OBJECT_H_

#define PyObject_HEAD \
    int refCount;
    struct tagPyTypeObject *type

#define PyObject_HEAD_INIT(typePtr)\
    0, typePtr

typedef struct tagPyObject
{
    PyObject_HEAD;
}PyObject;


typedef void (*PrintFun)(PyObject *Object);
typedef PyObject *(*AddFun)(PyObject *left, PyOjbect *right);

typedef struct tagPyTypeObject
{
    PyObject_HEAD;
    char *name;
    PrintFun print;
    AddFun add;
}PyTypeObject;

extern PyTypeObject PyType_Type;

#endif
