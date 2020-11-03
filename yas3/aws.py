

def test_aws_acl(acl_string):
    if acl_string not in ('private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read',
                               'bucket-owner-read', 'bucket-owner-full-control'):
        raise ValueError('ACL string must be one of: ',
                            ('private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read',
                            'bucket-owner-read', 'bucket-owner-full-control'))
    return True
