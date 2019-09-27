# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

import json


def json_encode(post_data):
    def get_object_dict(obj):
        if (type(obj) == bytes):
            raise TypeError

        objDict = dict()
        for k, v in obj.__dict__.items():
            if not k.startswith("_x_"):
                objDict[k] = v

        return objDict

    return json.dumps(post_data, default=get_object_dict,
                      sort_keys=True, indent=4)


def json_decode(json_str, obj_type):
    obj = obj_type()
    obj.__dict__ = json.loads(json_str)
    return obj
