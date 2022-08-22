package hash341;
import java.util.LinkedList;
public class sTable extends Slot{
    public City[] map;
    Hash24 h;
    int tsize;
    LinkedList<City> arr;
    

    public sTable(int ncs, City c){
        super();
        arr=new LinkedList<City>();
        nCity=ncs;
        tsize=ncs*ncs;
        map = new City[tsize];
        h = new Hash24();
        nHash=1;
        int hash = h.hash(c.name)%tsize;
        map[hash]=c;

    }

    @Override
    public void add(City c){
        int hash = h.hash(c.name)%tsize;
        if(map[hash]!=null){
            rehash();
        } else{
            map[hash]=c;
        }

    }

    public void rehash(){
        nHash++;
        h = new Hash24();
        for(int i=0;i<tsize;i++){
            if(map[i]!=null){
                arr.addFirst(map[i]);
                map[i]=null;
            }
        }
        while(arr.size()>1){
            City c=arr.peekFirst();
            int hash = h.hash(c.name)%tsize;
            if(map[hash]!=null){
                rehash();
            } else{
                map[hash]=c;
            }
            arr.pop();

        }
        

    }

    @Override
    public String toString(){
        String outs="";
        outs+=nHash+"\n";

        for(int i=0;i<tsize;i++){
            if(map[i]!=null){
                outs+=map[i].toString();
            }
        }

        return outs;
    }
    
}
