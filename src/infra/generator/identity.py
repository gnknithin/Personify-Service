from uuid import UUID, uuid4


class IdentityGenerator():

    @staticmethod
    def get_random_uuid4() -> UUID:
        """return random UUID of type uuuid4

        Returns:
            UUID: UUID
        """
        return uuid4()

    @staticmethod
    def get_random_id() -> str:
        """return a random string of object length 32

        Returns:
            str: random string of 32 characters length
        """
        return IdentityGenerator.get_random_uuid4().hex

    @staticmethod
    def get_random_id_of_object_length() -> str:
        """return a random string of object length 24

        Returns:
            str: random string of 24 characters length
        """
        return IdentityGenerator.get_random_id()[0:24]
