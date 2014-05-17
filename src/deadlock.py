MAX = [9,6,3]


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

    def is_secure(self, index):
        job = [j for j in self.available]
        
        job = self.sum(job, self.assigned[index])
        self.finished[index] = True

        for i in range(len(self.finished)):
            if self.finished[i] == False and self.requests[i] <= job:
                job = self.sum(job, self.assigned[i])
                self.finished[i] = True
                i += 1
        is_secure = True
        for i in range(len(self.finished)):
            if self.finished[i] == False:
                is_secure = False
                break
        print "Seguridad: ", self.finished, "=", is_secure
        return is_secure

    def get_resources(self, request, index):
        """status returned:
            0 = Error de solicitud exagerada
            1 = suspender proceso
            2 = dar recursos
            3 = recuperar estado previo"""
        if request > self.needed[index]:
            print "[ERROR] Se estan solicitando mas recursos de los necesarios\n"
            return 0
        if request > self.available:
            print "[proceso: %s, no se puede satisfacer la peticion %s]" % (self.needed[index], request)
            return 1
        else:
            self.assigned_backup = self.assigned[index]
            self.available_backup = self.available[index]
            self.requests_backup = self.requests[index]

            self.assigned[index] = self.sum(self.assigned[index], request)
            self.available = self.difference([self.available], [request])[0]
            # self.needed[index] = self.difference([self.needed[index]], [request])
            self.requests[index] = [0]*len(request)

            if self.is_secure(index):
                print "ES SEGURO", request
                return 2
            else:
                # print "no es seguro....", self.available
                # self.print_matrixes()
                # raise Exception
                self.assigned[index] = self.assigned_backup # [0]*len(request)
                self.requests[index] = self.requests_backup
                self.available = self.sum(self.available, request)
                return 3

    def print_matrixes(self):
        print "Needed\t\tAssigned\trequested"
        for idx in range(len(self.needed)):
            print "%s\t%s\t%s" % (self.needed[idx],self.assigned[idx], self.requests[idx])
        print
        print "Total: %s\tAvailable: %s\n\n" % (self.max, self.available)

    def run(self):
        band = True
        j = 1
        for i, pi in enumerate(self.requests):
            print "\n=================ANALIZANDO PETICION:%s================" % pi
            self.print_matrixes()
            ans = self.get_resources(pi, i)
            if ans == 2:
                print "estadop seguro"
                band = False
                break
            elif ans == 3:
                print "no es seguro, siga"
                #break
        #print "\n\nEstado SEGURO"



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
    assigned = [
       [1,0,2,1,1],
       [2,0,1,1,0],
       [1,1,0,1,0],
       [1,1,1,1,0]
       ]
    needed = [
       [1,2,2,1,2],
       [2,2,2,1,0],
       [2,1,3,1,0],
       [1,1,2,2,1]
       ]
    needed = [
        [2,3,1],
        [3,1,2],
        [1,0,5],
    ]
    assigned = [
        [1,3,0],
        [3,1,1],
        [0,0,3],
    ]
