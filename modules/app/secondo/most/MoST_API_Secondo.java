package most;



import sj.lang.ESInterface;
import sj.lang.IntByReference;
import sj.lang.ListExpr;
import communication.optimizer.*;

public class MoST_API_Secondo {

    private static OptimizerInterface OptInt = new OptimizerInterface();
    private static ESInterface Secondointerface = new ESInterface();
    
	public static void main(String[] args) {
		boolean ok;

		// Connection with SECONDO 
	    Secondointerface.setHostname("deti-lei-1.ua.pt");
	    Secondointerface.setPort(1234);
	    Secondointerface.useBinaryLists(true);
            ok = Secondointerface.connect();
            
            
            
        if(!ok) {
            System.err.println("<MoST> You are not connected to a Secondo Server");
            return;
        }
        
        System.out.println("Connected to Secondo.");
	OptInt.setHost("deti-lei-1.ua.pt");
	OptInt.setPort(1235);
        ok = OptInt.connect();
        if (ok) 
            System.out.println("connect to optimizer");
            
        String name = retrieveDBName();
        System.out.print(name);
        
        // execute a command
        String cmd = "open database JMM";
        
        System.out.println(cmd);
        ok = execCommand(cmd, Secondointerface);
 	
        cmd = "query interpolate2([const region value (((( 0 0 ) ( 0 4 ) ( 0 8 ) ( 2 8 ) ( 2 2 ) ( 4 2 ) ( 4 8 ) ( 6 8 ) ( 6 0 ))))], [const instant value \"2014-01-01 00:00\"], [const region value (((( 6 8 ) ( 6 2 ) ( 6 0 ) ( 4 0 ) ( 4 6 ) ( 2 6 ) ( 2 0 ) ( 0 0 ) ( 0 8 ))))], [const instant value \"2014-01-02 00:00\"])";
        ok = execCommand(cmd, Secondointerface);
 	
        
	    // Disconnect from Secondo
	Secondointerface.terminate();

	if(OptInt.isConnected()){
                OptInt.disconnect();
        }
        
       
  } 
     public static String retrieveDBName(){
      if(!Secondointerface.isInitialized()){
         return null;
      }
      ListExpr resultList = new ListExpr();
      IntByReference errorCode = new IntByReference(0);
      IntByReference errorPos = new IntByReference(0);
      StringBuffer errorMessage = new StringBuffer();
      Secondointerface.secondo("query getDatabaseName()",
                                   resultList,
                                   errorCode, errorPos, errorMessage);
       if(errorCode.value!=0){
          return null;
       }
       if(resultList.listLength()!=2){
          return null;
       }
       if(resultList.second().atomType() != ListExpr.STRING_ATOM){
          return null;
       }  
       String name = resultList.second().stringValue().trim();
       return name.length()==0?null:name;  

   } 

        
	/** Executes a command in sos syntax **/
	static boolean execCommand(String cmd, ESInterface Secondointerface){
	    if(!Secondointerface.isInitialized()){
	    		System.err.println("<MoST> You are not connected to a Secondo Server");
	            return false;
	    }
          
            ListExpr resultList = new ListExpr();
            IntByReference errorCode = new IntByReference(0);
            IntByReference errorPos = new IntByReference(0);
            StringBuffer errorMessage = new StringBuffer();
            
            Secondointerface.secondo(cmd, resultList, errorCode, errorPos, errorMessage);
	    
	    System.out.println("Command: ".concat(cmd));
            System.out.println("Result: ");
            System.out.println(resultList);
	    System.out.printf("errorcode=%d, errorPos=%d, errorMessage=%s\n\n", errorCode.value, errorPos.value, errorMessage.toString());
	    
	    return errorCode.value==0;
            
	}
}
