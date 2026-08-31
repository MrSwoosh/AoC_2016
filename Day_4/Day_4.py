# Date: 23-9-2025
## Part 1

count = 0

with open("dataset_day_4", 'r') as file:
    for row in file:
        row = row.strip()

        row = row[:-1]

        name, hash_check = row.split("[")

        if all(i in name for i in hash_check):
            pass
        else:
            continue

        if all(name.count(hash_check[i]) >= name.count(hash_check[i+1]) for i in range(len(hash_check) - 1)):
            pass
        else:
            continue

        good = True
        for i in range(len(hash_check) - 1):
            if name.count(hash_check[i]) == name.count(hash_check[i+1]):
                if hash_check[i] < hash_check[i+1]:
                    pass
                else:
                    good = False

        if good:
            for i in range(len(name)-1, -1, -1):
                if name[i] == "-":
                    count += int(name[i+1:])
                    break

print(f"Valid rooms: {count}")


## Part 2


count = 0



letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

with open("dataset_day_4", 'r') as file:
    for row in file:
        row = row.strip()

        row = row[:-1]

        name, hash_check = row.split("[")

        if all(i in name for i in hash_check):
            pass
        else:
            continue

        if all(name.count(hash_check[i]) >= name.count(hash_check[i+1]) for i in range(len(hash_check) - 1)):
            pass
        else:
            continue

        good = True
        for i in range(len(hash_check) - 1):
            if name.count(hash_check[i]) == name.count(hash_check[i+1]):
                if hash_check[i] < hash_check[i+1]:
                    pass
                else:
                    good = False

        number = 0
        if good:
            for i in range(len(name)-1, -1, -1):
                if name[i] == "-":
                    number = int(name[i+1:])
                    break

            name = name.replace(str(number), "")
            name = name.replace("-", " ")

            for i in range(len(name)):
                if name[i] != " ":
                    val = letters.index(name[i])
                    val += number
                    val = val % 26
                    name = name[:i] + letters[val] + name[i+1:]

            if "storage" in name:
                if "northpole" in name:
                    print(name + " " + str(number))

print(f"Valid rooms: {count}")

