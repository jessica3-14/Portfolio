package hash341;
import java.io.*;
import java.util.*;

public class CityTable implements Serializable {
    Slot[] tab;
    int nCities;
    Hash24 h1;
    int size;
    public CityTable(){

    }
    public CityTable (String fname, int tsize) {
        nCities=0;
        Scanner ifs=null;

        //Open file
        try{
            ifs = new Scanner(new FileReader(fname));
        }catch (FileNotFoundException e) 
		{
			System.out.println("File not found");
			e.printStackTrace(); // prints error(s)
			System.exit(0); // Exits entire program
		}

        //Initialize some shit
        tab = new Slot[tsize];
        for(int i=0;i<tsize;i++){
            tab[i]= new Slot();
        }
        h1 = new Hash24();
        h1.dump();
        System.out.println("Primary has table size: "+tsize);
        int[] nCollisions = new int[25];
        for(int i=1;i<25;i++){
            nCollisions[i]=0;
        }
        int[] nHashes = new int[21];
        for(int i=1;i<21;i++){
            nHashes[i]=0;
        }
        size=tsize;
        

        //Read in cities
        
        while(ifs.hasNextLine()){
            String line = ifs.nextLine();
            ifs.nextLine();
            nCities++;
            int hash = h1.hash(line)%tsize;
            
            tab[hash].nCity++;
            nCollisions[tab[hash].nCity-1]++;
            if(tab[hash].nCity>1){
                nCollisions[tab[hash].nCity-2]--;
            }
            
            

        }
        

        ifs.close();
        try{
            ifs = new Scanner(new FileReader(fname));
        }catch (FileNotFoundException e) 
		{
			System.out.println("File not found");
			e.printStackTrace(); // prints error(s)
			System.exit(0); // Exits entire program
		}
        City entryc;
        int maxCol=0;
        int maxDex=0;

        while(ifs.hasNextLine()){
            String line = ifs.nextLine();
            String line2 = ifs.nextLine();
            StringTokenizer tkz = new StringTokenizer(line2);
            float f1 = Float.parseFloat(tkz.nextToken());
            float f2 = Float.parseFloat(tkz.nextToken());
            int hash = h1.hash(line)%tsize;

            entryc = new City(line,f1,f2);

            if(tab[hash].nCity==1){
                entryc.nCity=1;
                tab[hash]=entryc;
                //nCollisions[0]++;
            } else if(tab[hash] instanceof sTable){
                int b4 = tab[hash].nHash;
                tab[hash].add(entryc);
                if(tab[hash].nHash!=b4){
                    nHashes[b4]--;
                    nHashes[tab[hash].nHash]++;
                }
                
            } else{
                tab[hash] = new sTable(tab[hash].nCity,entryc);
                nHashes[1]++;
                if(tab[hash].nCity>maxCol){
                    maxCol=tab[hash].nCity-1;
                    maxDex=hash;
                }
            }

        }

        
        System.out.println("Max number of collisions: "+maxCol);
        sTable ten=(sTable) tab[maxDex];
        for(int i=0;i<ten.tsize;i++){
            if(ten.map[i]!=null){
                System.out.println(ten.map[i].name);
            }
        }
        System.out.println("Number of slots for each number of collisions: ");
        for(int i=0;i<25;i++){
            System.out.println(i+": "+nCollisions[i]);
        }
        System.out.println("Number of slots for each number of hashes: ");
        float sum=0;
        float cnt=0;
        for(int i=1;i<21;i++){
            System.out.println(i+": "+nHashes[i]);
            sum+=i*nHashes[i];
            cnt+=nHashes[i];
        }
        System.out.println("Average hashes is: "+sum/cnt);
        
        
        

    };
    public City find(String name){
        int hash = h1.hash(name)%size;
        if(tab[hash] instanceof City){
            return (City) tab[hash];
        } else if (tab[hash] instanceof sTable){
            sTable ten = (sTable) tab[hash];
            int h2 = ten.h.hash(name);
            if(ten.map[h2] instanceof City){
                return (City) ten.map[h2];
            }
        }
        return null;
    };
    public void writeToFile(String name){
       try{
        FileOutputStream out = new FileOutputStream(name);
        ObjectOutputStream oout = new ObjectOutputStream(out);

         // write something in the file
        
            oout.writeObject(this);
            oout.close();
        }catch (Exception ex) {
            ex.printStackTrace();
         }
         // close the stream
        
    }
    public static CityTable readFromFile(String name){
        try{
        FileInputStream fis = new FileInputStream(name);  
        ObjectInputStream ois = new ObjectInputStream(fis);  
        CityTable ct= (CityTable) ois.readObject();  
        ois.close();  
        return ct;
        }
        catch (Exception ex) {
            ex.printStackTrace();
         }
        return new CityTable("", 0);
    }
    
}
