import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;

public class ParseMetaData {
  
  public static void main(String[] args){
    
    ArrayList<String> metaFields = new ArrayList<String>();
    String bookDelineator=new String("||||||||||||||||||||||||||||||||");
    metaFields.add("Title:");
    metaFields.add("Author:");
    metaFields.add("Posting Date:");
    metaFields.add("Release Date:");
    metaFields.add("Language:");
    metaFields.add("Character set encoding:");
    
    try {
      
      //open input file
      FileInputStream fstream = new FileInputStream(args[0]);
      BufferedReader buffer=new BufferedReader(new InputStreamReader(fstream));
      
      //open output file
      PrintWriter writer = new PrintWriter(args[1],"UTF-8");
      
      String line;
      
      while((line=buffer.readLine())!=null){
        
        // check to see if line contains a book delineator
        if (line.contains(bookDelineator)){
          
          //write out to output file
          //System.out.println(line);
          writer.println(line);
        }
        else{
          
          //check to see if it contains one of the keyword arguments
          //if so write out that line and return (no need to write lines out 
          //twice if they match multiple metaFields
          for (int i=0;i<metaFields.size();i++){
            if(line.contains(metaFields.get(i))){
              //System.out.println(line);
              writer.println(line);
              break;
            }
          }
        }
      }
      writer.close();
      buffer.close();
    }
    catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }

}
