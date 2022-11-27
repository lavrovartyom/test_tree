import itertools as I
import operator as O


class TreeStore:
    def __init__(self, items):
        self.__items = {item['id']: item for item in items}
        self.__chlds = {
            pid: [item['id'] for item in items] for pid, items in I.groupby(self.__items.values(), O.itemgetter('parent'))
        }

    def getAll(self):
        return list(self.__items.values())

    def getItem(self, ident, default=None):
        return self.__items.get(ident, default)

    def getChildren(self, ident):
        return list(map(self.getItem, self.__chlds.get(ident, [])))

    def getAllParents(self, ident):
        parent_id = self.getItem(ident, {}).get('parent')
        if parent_id is not None:
            parent = self.getItem(parent_id)
            return [parent] + self.getAllParents(parent['id'])
        return []


def main():
    items = [
        {'id': 1, 'parent': None},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 3, 'parent': 1, 'type': 'test'},
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 5, 'parent': 2, 'type': 'test'},
        {'id': 6, 'parent': 2, 'type': 'test'},
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}
    ]

    ts = TreeStore(items)

    import pprint
    pprint.pprint(ts.getAll())

    assert ts.getItem(7) == {'id': 7, 'parent': 4, 'type': None}

    assert ts.getChildren(4) == [
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}]

    assert ts.getChildren(5) == []

    assert ts.getAllParents(7) == [
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 1, 'parent': None}
    ]
    print('Тесты пройдены успешно')


if __name__ == '__main__':
    main()
