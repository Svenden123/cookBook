class Meal:
    def __init__(self, name='', items=None):
        self.name = name
        self.items = items

    def transform(self):
        return {self.name: [item.transform() for item in self.items]}


class Item:
    def __init__(self, name='', count=0, unit=''):
        self.name = name
        self.count = count
        self.unit = unit

    def transform(self):
        return {'ingridient_name': self.name, 'quantity': self.count, 'measure': self.unit}


def get_shop_list_by_dishes(dishes, person_count):
    items = {}
    for mealName in dishes:
        mealItems = cook_book[mealName]
        for mealItem in mealItems:
            if not items.get(mealItem['ingridient_name']):
                items[mealItem['ingridient_name']] = {'measure': mealItem['measure'], 'quantity': mealItem['quantity']*person_count}
            else:
                items[mealItem['ingridient_name']]['quantity'] += mealItem['quantity']*person_count
    return items


buffMeal = None
buffItems = []
meals = []
total = 1
fileName = 'cookbook.dat'

with open(fileName) as file:
    array = [row.strip() for row in file]
    for line in array:
        if not line:
            continue

        parts = [part.strip() for part in line.split('|')]

        if len(parts) == 3:
            buffItems.append(Item(parts[0], int(parts[1]), parts[2]))
        elif len(parts) == 1:
            if parts[0].isdigit():
                total = int(parts[0])
            else:
                if not buffMeal == None:
                    buffMeal.items = buffItems[:total]
                    buffItems = []
                    meals.append(buffMeal)
                buffMeal = Meal(parts[0])
        else:
            print(fileName+' file was ruined, check it')
            exit(1)

buff = [meal.transform() for meal in meals]
cook_book = {}
for meal in buff:
    cook_book.update(meal)

shopList = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
