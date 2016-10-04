import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;

public class LineCount {
  
  public static void main(String[] args){
    
    try {
      
      //Read input file one line at a time
      //and count words
      FileInputStream fstream = new FileInputStream(args[0]);
      BufferedReader buffer=new BufferedReader(new InputStreamReader(fstream));
      String line;
      int i;
      int count=0;
      while((line=buffer.readLine())!=null){
        
        count=count+1;
      }
      buffer.close();
    }
    catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

}
