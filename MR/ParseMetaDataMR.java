import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class ParseMetaDataMR {
  
  public static class LineMapper extends Mapper<Object, Text, Object, Text> {
    
    private ArrayList<String> metaFields = new ArrayList<String>();
    private String bookDelineator=new String("||||||||||||||||||||||||||||||||");
    //private String colon=new String(":");
    
    protected void setup(Context context) throws IOException, InterruptedException {
      
      metaFields.add("Title:");
      metaFields.add("Author:");
      metaFields.add("Posting Date:");
      metaFields.add("Release Date:");
      metaFields.add("Language:");
      metaFields.add("Character set encoding:");
    }
    
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      
      // check to see if line contains a book delineator
      if (value.find(bookDelineator)!=-1){
        Text temp=new Text(bookDelineator);
        context.write(key, temp);
      }
      else{
        
        //check to see if it contains one of the keyword arguments
        //if so write out that line and return (no need to write lines out 
        //twice if they match multiple metaFields
        for (int i=0;i<metaFields.size();i++){
          if(value.find(metaFields.get(i))!=-1){
            context.write(key, value);
            return;
          }
        }
        
        //check for any possibly missed metaFields by looking for ":" character
        //if(value.find(colon)!=-1){
        //  context.write(key, value);
        //}
        
      }
    }
  }
  
  public static class PassThroughReducer extends Reducer<Object, Text, Object, Text> {
    
    public void reduce(Object key, Text values, Context context) throws IOException, InterruptedException {
      
      context.write(key, values);
    }
  }
  
  public static void main(String[] args) throws Exception {
    
    System.out.println(args[0]);
    
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "ParseMetaDataMR");
    job.setJarByClass(ParseMetaDataMR.class);
    job.setMapperClass(LineMapper.class);
    job.setReducerClass(PassThroughReducer.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}