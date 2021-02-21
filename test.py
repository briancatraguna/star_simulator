class Test:
    x = 0
    def config(self,change):
        self.x = change

test = Test()
print(test.x)
test.config(3)
print(test.x)