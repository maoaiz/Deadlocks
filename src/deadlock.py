# -*- coding: utf-8 -*-
class Deadlock:
    def __init__(self, total_system):
        self.RESOURCES = total_system

    def execute(self, needed, assigned):
        self.needed = needed
        self.assigned = assigned
        self.finished = [False]*len(assigned)
        self.requests = self.calc_requests()
        self.available = self.calc_available()
        self.run()

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

    def less_equal(self, a, b):
        ans = [i for i, j in zip(a, b) if i > j]
        if ans == []:
            return True
        else:
            return False

    def calc_requests(self):
        return self.difference(self.needed, self.assigned)

    def calc_available(self):
        a = self.assigned
        res = []
        for j in range(len(a[0])):
            tmp = 0
            for i in range(len(a)):
                tmp += a[i][j]
            res.append(self.RESOURCES[j] - tmp)
        return res

    def dispatch(self):
        print
        print "##################################################################"
        self.print_matrixes()
        for i in range(len(self.needed)):
            r = self.requests[i]
            self.available = self.difference([self.available], [r])[0]
            self.assigned[i] = self.sum(self.assigned[i], r)
            self.requests[i] = [0]*len(r)
            
            print "despachando...", self.needed[i]
            self.available = self.sum(self.available, self.assigned[i])
            self.assigned[i] = [0]*len(r)

            self.print_matrixes()
        print "##################################################################"
        print

    def is_secure(self, index):
        # print self.available
        # print self.available_backup

        job = [j for j in self.available]
        # job = self.sum(job, self.assigned[index])
        # self.finished[index] = True

        for i in range(len(self.finished)):
            if self.finished[i] == False and self.less_equal(self.requests[i], job):
                job = self.sum(job, self.assigned[i])
                self.finished[i] = True
                i += 1
        is_secure = True
        for i in range(len(self.finished)):
            if self.finished[i] == False:
                is_secure = False
                break
        print "Hay seguridad? %s = %s\n" % (self.finished, is_secure)
        return is_secure

    def get_resources(self, request, index):
        """status returned:
            0 = Error de solicitud exagerada
            1 = suspender proceso
            2 = dar recursos
            3 = recuperar estado previo"""
        if not self.less_equal(request, self.needed[index]):
            print "[ERROR] Se estan solicitando mas recursos de los necesarios\n"
            return 0
        if not self.less_equal(request, self.available):
            print "[EN ESPERA] Proceso: %s, no se puede despachar la peticion %s" % (self.needed[index], request)
            return 1
        else:
            print "[SE PUEDE DESPACHAR] la petición %s si se puede despachar.\n" % request
            self.assigned_backup = self.assigned[index]
            self.available_backup = self.available
            self.requests_backup = self.requests[index]

            self.assigned[index] = self.sum(self.assigned[index], request)
            self.available = self.difference([self.available], [request])[0]
            # self.needed[index] = self.difference([self.needed[index]], [request])
            self.requests[index] = [0]*len(request)

            if self.is_secure(index):
                # self.available = self.available_backup
                print "Es estado es SEGURO, todos los procesos se pueden despachar sin que haya interbloqueo.\n"
                self.dispatch()
                return 2
            else:
                self.assigned[index] = self.assigned_backup
                self.requests[index] = self.requests_backup
                self.available = self.sum(self.available, request)
                return 3

    def print_matrixes(self):
        print "_____________________________________________"
        print "Needed\t\tAssigned\trequested"
        for idx in range(len(self.needed)):
            print "%s\t%s\t%s" % (self.needed[idx],self.assigned[idx], self.requests[idx])
        print "_____________________________________________"
        print "Resources:"
        print "Total: %s\tAvailable: %s\n" % (self.RESOURCES, self.available)

    def run(self):
        for i, pi in enumerate(self.requests):
            print "\n=================ANALIZANDO PETICION:%s================" % pi
            self.print_matrixes()
            ans = self.get_resources(pi, i)
            if ans == 2:
                break
            elif ans == 3:
                print "No es seguro"



if __name__ == "__main__":
    total_resources_system = [6, 5, 7, 6]
    b = Deadlock(total_resources_system)
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
    needed = [
        [3, 3, 2, 2],
        [1, 2, 3, 4],
        [1, 3, 5, 0],
    ]
    assigned = [
        [1, 2, 2, 1],
        [1, 0, 3, 3],
        [1, 2, 1, 0],
    ]
    b.execute(needed, assigned)
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
