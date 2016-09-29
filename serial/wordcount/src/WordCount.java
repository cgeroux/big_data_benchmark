import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;

public class WordCount {
  
  public static void main(String[] args){
    
    try {
      
      //Read input file one line at a time
      //and count words
      FileInputStream fstream = new FileInputStream(args[0]);
      BufferedReader buffer=new BufferedReader(new InputStreamReader(fstream));
      String line;
      String[] splits;
      Map<String,Integer> wordCounts=new HashMap<String,Integer>();
      int i;
      Integer checkValue;
      while((line=buffer.readLine())!=null){
        splits=line.split(" ");
        
        //DEBUGGING
        for (i=0;i<splits.length;i++){
          checkValue=wordCounts.get(splits[i]);
          if (checkValue==null){
            wordCounts.put(splits[i],1);
          }
          else{
            wordCounts.put(splits[i],checkValue+1);
          }
        }
      }
      buffer.close();
      
      //open output file and print out word counts
      PrintWriter writer = new PrintWriter(args[1],"UTF-8");
      Iterator it=wordCounts.entrySet().iterator();
      
      while(it.hasNext()){
        Map.Entry pair=(Map.Entry)it.next();
        writer.println(pair.getKey()+":"+pair.getValue().toString());
      }
      writer.close();
    }
    catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

}
