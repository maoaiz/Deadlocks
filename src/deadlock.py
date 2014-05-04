MAX = [9, 3, 6]


class Deadlock:
    def __init__(self, needed, assigned):
        self.max = MAX
        self.needed = needed
        self.assigned = assigned
        self.finished = [False]*len(assigned)
        self.requests = self.calc_requests()
        self.available = self.calc_available()

    def difference(self, a, b):
        """Retorna una matriz con la resta de los elementos de dos matrices"""
        print a, " - ", b
        res = []
        for i in range(len(a)):
            tmp = []
            for j in range(len(a[i])):
                tmp.append(a[i][j]-b[i][j])
            res.append(tmp)
        return res

    def sum(self, a, b):
        """Retorna una lista con la suma de los elementos de dos listas"""
        res = []
        if len(a) == len(b):
            for i in range(len(a)):
                res.append(a[i] + b[i])
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
        job = []
        for j in self.available:
            job.append(j)
        for i in range(len(self.finished)):
            if self.finished[i] == False and self.needed[i] <= job:
                job = self.sum(job, self.assigned[i])
                self.finished[i] = True
                i += 1
        is_secure = True
        for i in range(len(self.finished)):
            if self.finished[i] == False:
                is_secure = False
                break
        return is_secure

    def get_resources(self, request, index):
        """status returned:
            0 = Error de solicitud exagerada
            1 = suspender proceso
        """
        if request > self.needed[index]:
            print "[ERROR] Se estan solicitando mas recursos de los necesarios\n"
            return 0
        if request > self.available:
            print "No se puede satisfacer. proceso en espera", request
            return 1
        else:
            self.available = self.difference([self.available], [request])[0]
            self.assigned[index] = self.sum(self.assigned[index], request)
            self.needed[index] = self.difference([self.needed[index]], [request])
            print "Las variables han sido modificadas"
            if self.is_secure():
                print "ES SEGURO", request
                return 2
            else:
                print "NO ES SEGURO", request
                return 3

    def run(self):
        for i, pi in enumerate(self.requests): 
            print self.get_resources(pi, i)
            print "self.available", self.available
            print "self.needed", self.needed
            print "self.assigned", self.assigned
            print "self.requests", self.requests
            #break



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
