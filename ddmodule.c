#include <Python.h>
#include <stdint.h>

// !!
// !! I'm currently ignoring endianness, this works on my little-endian machine
// !! but most likely would not work on another machine.
// !!

static inline int16_t
_decode_16(int number)
{   
    return number % 256 | number / 256;
}

static inline int32_t
_decode_32(int number)
{                          /* 2 ^ 16 */
    return _decode_16(number % 65536) | _decode_16(number / 65536); 
}

typedef struct Buffer {
    int len, occ;
    char * pool;
} Buffer;

Buffer * Create_Buffer(int len)
{
    Buffer * b;
    b = malloc(sizeof(Buffer));
    b->len = len;
    b->occ = 0;
    b->pool = malloc(len);
    return b;
}

void Write(Buffer * buffer, void * data, int len)
{
    char * new_pool;
    if (buffer->occ + len > buffer->len) {
        fflush(stdout);
        buffer->len *= 2;
        new_pool = malloc(buffer->len);
        memcpy(new_pool, buffer->pool, buffer->occ);
        free(buffer->pool);
        buffer->pool = new_pool;
    }

    memcpy(buffer->pool + buffer->occ, (char *) data, len);
    buffer->occ += len;
}

void WriteF(Buffer * buffer, int n, int len, FILE * file)
{
    char * data;
    data = malloc(n * len);
    len = fread(data, n, len, file);
    Write(buffer, data, n * len);
    free(data);
}

static const char * texts[] = { 
    "Somebody once",
    "told me",
    "the world",
    "is gonna",
    "roll me",
    "I aint",
    "the sharpest",
    "tool in",
    "the shed",
    "etc"
};

static PyObject *
create_leaderboards(PyObject * self, PyObject * args)
{
    FILE * source;
    long source_len;
    const char * filename;
    char * cur_text;
    Buffer * buffer;
    PyObject * return_object;
    uint16_t string_len = 0;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;

    buffer = Create_Buffer(1024);

    source = fopen(filename, "rb");

    fseek(source, 0, SEEK_END);
    source_len = ftell(source);
    fseek(source, 0, SEEK_SET);

    WriteF(buffer, 1, 7, source);
    WriteF(buffer, 1, 72, source);

    for (int32_t i = 1; i <= 100; i++) {
        WriteF(buffer, 1, 4, source);

        cur_text = texts[(i - 1) % 10];
        string_len = strlen(cur_text);
        Write(buffer, &string_len, 2);

        Write(buffer, cur_text, string_len);

        Write(buffer, &i, 4);

        fseek(source, 2 + string_len + 4, SEEK_CUR);
        WriteF(buffer, 19, 4, source);
    }

    WriteF(buffer, 1, source_len - ftell(source), source);
    return_object = PyBytes_FromStringAndSize(buffer->pool, buffer->occ);

    free(buffer->pool);
    free(buffer);
    fclose(source);

    return return_object;
}

static PyMethodDef
dd_methods[] = {
    { 
          "create_leaderboards" // Name
        , create_leaderboards   // Function Pointer
        , METH_VARARGS          // Flags
        , "Create Leaderboards HTTP Package" // DocString // Can be empty???
    },

    { NULL, NULL, 0, NULL } // Sentinel
};

static struct PyModuleDef
dd_module_definition = {
      PyModuleDef_HEAD_INIT // Base
    , "dd"          // Name
    , "I didn't want to edit bytes directly in python" // Docstring
    , -1             // Size of global state
    , dd_methods     // Methods
};

PyObject *
PyInit_dd( void )
{
    Py_Initialize();
    return PyModule_Create(&dd_module_definition);
}
