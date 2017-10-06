#include "Python.h" 
#define PUBKEY_BYTES 32
#define PRIVKEY_BYTES 64
#define SEED_BYTES 32
#define SIGNATURE_BYTES 64


extern int ed25519_create_seed(unsigned char*);
extern void ed25519_create_keypair(unsigned char* , unsigned char* , const unsigned char*);
extern void ed25519_sign(unsigned char*, const unsigned char*, size_t, const unsigned char*, const unsigned char*);
extern int ed25519_verify(const unsigned char*, const unsigned char*, size_t, const unsigned char*);
 
PyObject* create_keypair(PyObject* self){

 unsigned char pubkey[PUBKEY_BYTES];
 unsigned char privkey[PRIVKEY_BYTES];
 unsigned char seed[SEED_BYTES];
 int code;
 
 if ( (code = ed25519_create_seed(seed)) < 0 ) {
    Py_INCREF(Py_None);
    return Py_None;
 }

 ed25519_create_keypair(pubkey, privkey, seed);
 return Py_BuildValue("(y#y#)", pubkey, PUBKEY_BYTES, privkey,PRIVKEY_BYTES);
}

PyObject* sign(PyObject* self, PyObject* args){
  const unsigned char* message;
  const unsigned char* pubkey;
  const unsigned char* privkey;
  int message_size, pubkey_size, privkey_size;
  unsigned char signature[SIGNATURE_BYTES];

  if(!PyArg_ParseTuple(args, "y#y#y#", &message, &message_size, &pubkey, &pubkey_size, &privkey, &privkey_size)){
    Py_INCREF(Py_None);
    return Py_None;
  }

 ed25519_sign(signature, message, message_size, pubkey, privkey);

 return Py_BuildValue("y#", signature, SIGNATURE_BYTES);

}

PyObject* verify(PyObject* self, PyObject* args){
  const unsigned char* message;
  const unsigned char* pubkey;
  const unsigned char* signature;
  int message_size, pubkey_size, signature_size;

  if(!PyArg_ParseTuple(args, "y#y#y#", &message, &message_size, &signature, &signature_size, &pubkey, &pubkey_size)){
    Py_INCREF(Py_None);
    return Py_None;
  }

 return Py_BuildValue("i", ed25519_verify(signature, message, message_size, pubkey));


}

static PyMethodDef myMethods[] = {
  {"create_keypair", create_keypair, METH_NOARGS, "create a keypair"},
  {"sign", sign, METH_VARARGS, "sign signeaute using keypair"},
  {"verify", verify, METH_VARARGS, "verify"},
  {NULL, NULL, 0, NULL}
};

struct PyModuleDef myModule = {
      PyModuleDef_HEAD_INIT,
      "ed25519_sha3",
      NULL,
      -1,
      myMethods
};

PyObject* PyInit_ed25519_sha3(void) {
    return PyModule_Create(&myModule);
}

