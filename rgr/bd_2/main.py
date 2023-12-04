import controller
import model

model.connect()

controller.menu()

model.disconnect()



# model.insert(1, ['asd', 'rew', True])
# model.insert(2, ['asd', 'rew', 5, 7])
# model.insert(3, ['asd', 'rew', 'fdsg', '988-12-12', 3])
# model.insert(4, ['asd', True, 'fdsg', 3])
# model.insert(5, ['1700-05-21', '1800-09-12', 3, 5, 98, 1500.45])
# model.insert(6, [5, 4])
# model.insert(7, [1, 6])

# model.delete('hotel', 'hotel_id', 9)
# model.delete('room', 'room_id', '13')

# print(model.select_by_key('room', 'arrival_date', '2015-01-07'))
# print(model.select_by_key('room', 'room_id', '1'))

# for row in model.select_by_table('hotel'):
#     print(row)

# model.update(1, ['qqqq', 'wwww', False], 14)
# model.update(2, ['qqqq', 'wwww', 4, 3], 10)
# model.update(3, ['qqqq', 'wwww', 'rrrr', '1444-09-09', 2], 11)
# model.update(4, ['qqq', True, 'www', 5], 10)
# model.update(5, ['2000-01-21', '2100-09-12', 1, 1, 1, 15.45], 14)

# model.insert(6, [2, 3])
# model.update(6, [4, 1], 2, 3)
# model.insert(7, [1, 6])
# model.update(7, [5, 2], 1, 6)

# model.generate(1, 5)
# model.generate(2, 3)
# model.generate(3, 50)
# model.generate(4, 10)
# model.generate(5, 50)
# model.generate(6, 10)
# model.generate(7, 10)

# lst = model.search(['category', 'room'], 'category_id', 'first.category_id = second.category_id')

# for i in lst[0]:
#     print(i)

# print(lst[1])

# print('\n', controller.print_request(6, quantity='5', offset='0'))
# print("\n", controller.print_request(6, id='3'))