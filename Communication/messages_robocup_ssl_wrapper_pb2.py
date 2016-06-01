# Under MIT License, see LICENSE.txt

__author__ = 'RoboCupULaval'

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from Communication.google.protobuf import descriptor as _descriptor
from Communication.google.protobuf import message as _message
from Communication.google.protobuf import reflection as _reflection
from Communication.google.protobuf import symbol_database as _symbol_database
from Communication.google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Communication.messages_robocup_ssl_detection_pb2
import Communication.messages_robocup_ssl_geometry_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages_robocup_ssl_wrapper.proto',
  package='',
  serialized_pb=_b('\n\"messages_robocup_ssl_wrapper.proto\x1a$messages_robocup_ssl_detection.proto\x1a#messages_robocup_ssl_geometry.proto\"`\n\x11SSL_WrapperPacket\x12&\n\tdetection\x18\x01 \x01(\x0b\x32\x13.SSL_DetectionFrame\x12#\n\x08geometry\x18\x02 \x01(\x0b\x32\x11.SSL_GeometryData')
  ,
  dependencies=[Communication.messages_robocup_ssl_detection_pb2.DESCRIPTOR,Communication.messages_robocup_ssl_geometry_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SSL_WRAPPERPACKET = _descriptor.Descriptor(
  name='SSL_WrapperPacket',
  full_name='SSL_WrapperPacket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection', full_name='SSL_WrapperPacket.detection', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='geometry', full_name='SSL_WrapperPacket.geometry', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=209,
)

_SSL_WRAPPERPACKET.fields_by_name['detection'].message_type = Communication.messages_robocup_ssl_detection_pb2._SSL_DETECTIONFRAME
_SSL_WRAPPERPACKET.fields_by_name['geometry'].message_type = Communication.messages_robocup_ssl_geometry_pb2._SSL_GEOMETRYDATA
DESCRIPTOR.message_types_by_name['SSL_WrapperPacket'] = _SSL_WRAPPERPACKET

SSL_WrapperPacket = _reflection.GeneratedProtocolMessageType('SSL_WrapperPacket', (_message.Message,), dict(
  DESCRIPTOR = _SSL_WRAPPERPACKET,
  __module__ = 'messages_robocup_ssl_wrapper_pb2'
  # @@protoc_insertion_point(class_scope:SSL_WrapperPacket)
  ))
_sym_db.RegisterMessage(SSL_WrapperPacket)


# @@protoc_insertion_point(module_scope)