import zaber
  
class Zaber() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.maxswitch = 1
        self.description = 'Zaber stage'
        self.name = 'Zaber focuser stage'
        self.minvalue = 0
        self.maxvalue = 50000
        self.connect()

    def connect(self) :
        print('connect Zaber stage')
        self.zaber_stage=zaber.ZaberStage()
        self.connected = True

    def connected(self,state) :
        print('connected',state)
        return state

    def canwrite(self) :
        return True

    def disconnect(self) :
        self.connected(False)

    def get_minvalue(self) :
        return self.minvalue

    def get_maxvalue(self) :
        return self.maxvalue

    def get_description(self) :
        return self.description

    def get_name(self) :
        return self.name

    def set_position(self,val) :
        print('setting value',val)
        self.zaber_stage.move(float(val)/1000.)

    def is_moving(self) :
        return False

    def get_position(self) :
        return int(self.zaber_stage.get_position()*1000.)

    def get_step(self) :
         return 1

