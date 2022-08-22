package hash341;

public class City extends Slot{
    public String name;
    public float latitude;
    public float longitude;
    public int loc;

    public City(String s, float l1, float l2){
        super();
        name=s;
        latitude=l1;
        longitude=l2;
    }
    
    @Override
    public String toString() {
        // TODO Auto-generated method stub
        String outs=name+"\n";
        outs+= latitude+" "+longitude+"\n";
        return super.toString()+outs;
    }

    
}
