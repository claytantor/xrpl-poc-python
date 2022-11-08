class XummApplicationDetailsSerializer(object):
    # init method or constructor
    def __init__(self, application_details):
        # 'quota': dict,
        # 'application': dict,
        # 'call': dict
        self.application = application_details.application
        self.quota = application_details.quota
        self.call = application_details.call
        
 
    # Sample Method
    def serialize(self):
        return {
            'application': {
                'name': self.application.name,
                'webhookurl': self.application.webhookurl,
                'uuidv4': self.application.uuidv4,
                'disabled': self.application.disabled,
                # 'redirecturis': self.application.redirecturis,
                # 'icon_url': self.application.icon_url,
            },
            'quota': {
                'ratelimit': self.quota.ratelimit,         
            },
            'call': {
                'uuidv4': self.call.uuidv4,
            }
        }