"""
Basic classes
"""
import json
from ._utils import make_serializable


class OmniaResource(object):
    """Basic resource object."""
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}


class OmniaResourceList(OmniaResource):
    """List of basic resource objects."""
    resources = list()

    @property
    def count(self):
        """int: Number of resources."""
        return len(self.resources)

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dicts representing the instance.
        """
        return [_.dump() for _ in self.resources]