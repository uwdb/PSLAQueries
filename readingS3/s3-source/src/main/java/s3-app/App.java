import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ListObjectsRequest;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.GetObjectRequest;
import java.io.*;

import java.util.Iterator;
import java.util.List;

public class App 
{
	AmazonS3 s3;
	public static void main(String[] args) {
    App base = new App();
    
    try{
    base.readFromS3("tpchssb", "4Workers/date-part1");
	}
	catch(Exception e){
	System.out.println("error on reading from bucket");
	}
}

 public void init(String accessKey, String secretKey) {
 	System.out.println(accessKey);
 	System.out.println(secretKey);
    s3 = new AmazonS3Client(new BasicAWSCredentials(accessKey, secretKey));
  }

 public void readFromS3(String bucketName, String key) throws IOException {
    S3Object s3object = s3.getObject(new GetObjectRequest(
            bucketName, key));
    System.out.println(s3object.getObjectMetadata().getContentType());
    System.out.println(s3object.getObjectMetadata().getContentLength());

    BufferedReader reader = new BufferedReader(new InputStreamReader(s3object.getObjectContent()));
    String line;
    while((line = reader.readLine()) != null) {
      //System.out.println(line);
    }
  }  
}
