class Tracker:

    TRACKER_FILE = "repo/tracker.info"

    def read_data(self, filename):
        with open(filename, 'r') as filecontent:
            data = filecontent.readlines()
        return data

    def write_file(self, data_file, data):
        with open(data_file, 'a') as file:
            file.writelines('\n'+data.lower())
            file.close()

    def read_load(self, name):
        val = self.read_data(self.TRACKER_FILE)
        for value in val:
            value = value.split(' ')
            if name.lower() == value[0].lower():
                return value[1].strip()
        return False

    def check_load(self, name):
        load = self.read_load(name)
        if not load:
            return True
        return False

    def write_status(self, name):
        if self.check_load(name) == False:
            return False
        self.write_file(tracker.TRACKER_FILE, name)
        return True

    def next(self, val):
        return int(val)+1

if __name__ == "__main__":

    tracker = Tracker()


    res = tracker.read_load("name")

    print(res)