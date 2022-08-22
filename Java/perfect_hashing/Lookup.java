import hash341.*;
import java.util.Scanner;
public class Lookup {
    public static void main(String[] args){
        CityTable ct=new CityTable();
        ct = ct.readFromFile("US_Cities_LL.ser");
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter City, ST or quit");
        String s = sc.nextLine();
        City temp;
        while(!s.equals("quit")){
            temp=ct.find(s);
            if(temp==null){
                System.out.println("City not found");
            } else{
                System.out.print(temp);
                System.out.println("https://google.com/maps/@"+temp.latitude+","+temp.longitude);
            }
            System.out.println("Enter City, ST or quit");
            s = sc.nextLine();

        }

    }
}
