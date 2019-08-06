from fields import TextField, BulletTextField, ImageField

class FieldFactory():

    @staticmethod
    def create(class_name, data):

        if isinstance(data, dict):
            all_type = {
                "TextField": TextField(**data),
                "BulletTextField": BulletTextField(**data),
                "ImageField": ImageField(**data) 
            }
        else:
            all_type = {
                "TextField": TextField(*data),
                "BulletTextField": BulletTextField(*data),
                "ImageField": ImageField(*data) 
            }

        return all_type[class_name]

