__author__ = 'antonioirizar'


class Instance:
    def __init__(self, size):
        self.size = size
        self.number_instances = 1

    def configure(self):
        configure = {
            'DryRun': False,
            'ImageId': 'ami-ed82e39e',
            'MinCount': self.number_instances,
            'MaxCount': self.number_instances,
            'InstanceType': self.size}
        return configure
