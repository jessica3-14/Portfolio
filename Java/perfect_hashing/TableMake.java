import hash341.*;

public class TableMake {
    public static void main(String[] args){
        CityTable ct = new CityTable("US_Cities_LL.txt",16000);
        ct.writeToFile("US_Cities_LL.ser");
    }
    
}
