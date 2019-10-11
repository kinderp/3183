from ..fields import TextField, BulletTextField, ImageField

class FieldFactory():

    @staticmethod
    def create(class_name, data):

        #if isinstance(data, dict):
        #    all_type = {
        #        "TextField": TextField(**data),
        #        "BulletTextField": BulletTextField(**data),
        #        "ImageField": ImageField(**data) 
        #    }
        #else:
        #    all_type = {
        #        "TextField": TextField(*data),
        #        "BulletTextField": BulletTextField(*data),
        #        "ImageField": ImageField(*data) 
        #    }

        if isinstance(data, dict):
                if class_name == 'TextField':
                        return TextField(**data)
                elif class_name == 'BulletTextField':
                        return BulletTextField(**data)
                elif class_name == 'ImageField':
                        return ImageField(**data)
        else:
                if class_name == 'TextField':
                        return TextField(*data)
                elif class_name == 'BulletTextField':
                        return BulletTextField(*data)
                elif class_name == 'ImageField':
                        return ImageField(*data)

        #return all_type[class_name]

