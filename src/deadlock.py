MAX = [9, 3, 6]


class Deadlock:
    def __init__(self, needed, assigned):
        self.max = MAX
        self.needed = needed
        self.assigned = assigned
        self.finished = len(assigned)
        self.requests = self.calc_requests()
        self.available = self.calc_available()

    def difference(self, a, b):
        res = []
        for i in range(len(a)):
            tmp = []
            for j in range(len(a[i])):
                tmp.append(a[i][j]-b[i][j])
            res.append(tmp)
        return res

    def sum(self, a, b):
        res = []
        for i in range(len(a)):
            tmp = []
            for j in range(len(a[i])):
                tmp.append(a[i][j]+b[i][j])
            res.append(tmp)
        return res

    def calc_requests(self):
        return self.difference(self.needed, self.assigned)

    def calc_available(self):
        a = self.assigned
        res = []
        for j in range(len(a[0])):
            tmp = 0
            for i in range(len(a)):
                tmp += a[i][j]
            res.append(self.max[j] - tmp)
        return res

    def is_secure(self):
        pass

    def get_resources(self, request, index):
        """status returned:
            0 = Error de solicitud exagerada
            1 = suspender proceso
        """
        if request > self.needed[index]:
            print "[ERROR] Se estan solicitando mas recursos de los necesarios\n"
            return 0
        if request > self.available:
            return 1
        else:
            self.available = self.difference(self.available, request)
            self.assigned = self.sum(self.assigned, request)
            self.needed = self.difference(self.needed, request)
            if self.is_secure():
                pass
            else:
                pass

    def run(self):
        pass



if __name__ == "__main__":
    needed = [
        [3, 2, 2],
        [6, 1, 3],
        [3, 1, 4],
        [4, 2, 2]
    ]
    assigned = [
        [1, 0, 0],
        [6, 1, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    b = Deadlock(needed, assigned)
    b.run()
