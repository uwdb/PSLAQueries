import os

random = [243, 245, 250, 272, 283, 290, 293, 298, 302, 306, 328, 331, 338, 340, 349, 351, 352, 358, 359, 375, 391, 399, 401, 405, 428, 436, 440, 442, 459, 460, 464, 465, 466, 473, 480, 502, 517, 519, 520, 521, 522, 524, 526, 538, 541, 542, 550, 555, 556, 564, 574, 594, 595, 598, 599, 608, 609, 617, 620, 639, 643, 644, 656, 663, 678, 679, 686, 692, 700, 706, 713, 714, 722, 725, 729, 734, 744, 750, 755, 758, 759, 765, 766, 770, 774, 782, 784, 792, 802, 807, 809, 813, 829, 837, 861, 870, 872, 878, 882, 891]
output = open(os.path.expanduser("runtimes-sample100.txt"), 'w');
with open("./runtimes_8computenodes.txt") as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        split = line.split(",")
        qid = split[0]
        number = int(split[1])
        time = split[2]

        if number in random:
            output.write(str(i) + "," + time)
            i = i + 1
