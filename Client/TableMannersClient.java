/*

To do: check that the stdIn string (such as "forward = 23432") is formatted correctly before sending it to the RPi

*/



import java.io.*;
import java.net.*;

public class TableMannersClient {

	public static void main(String args[]){
		
		String hostName = "10.44.15.35";
		int portNumber = 5800;
		
		try (
            Socket clientSocket = new Socket(hostName, portNumber);
            PrintWriter out =
                new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in =
                new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream()));
            BufferedReader stdIn =
                new BufferedReader(
                    new InputStreamReader(System.in))
        ) {
			clientSocket.setSoTimeout(1000);
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + 
				"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("Connection made. Sending Request");
			out.println("Requesting ds_pi_communication");

			boolean finished = false;
			while(!finished){
				String input = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
				System.out.println(input);
				if(input.equals("End of file")){
					finished = true;
				}
			}
			
			
			while(true){
				boolean goodInput = false;
				while(!goodInput){
					System.out.println("Type \"exit\" to exit.");
					String outLine = stdIn.readLine().trim().toLowerCase();
					if(outLine.equals("exit")){
						System.out.println("Exiting program.");
						out.println("");
						return;
					} else if (outLine.indexOf("=") != -1){
						out.println(outLine);
						goodInput = true;
					// ADD FEATURE TO CHECK RIGHT HALF IS A DOUBLE
					} else {
						System.out.println("\nInvalid input, try again.");
					}
				}
					System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + 
					"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
				boolean finished2 = false;
				while(!finished2){
					String input = in.readLine();					// KEEPS READING UNTIL LINE BREAK "\n"
					System.out.println(input);
					if(input.equals("End of file")){
						finished2 = true;
					}
				}
			}
		
			
			// Send request for table
			// readLine and printLine in a loop until "End of File" is recieved
			// wait for stdIn.readline()
			// send string to server
		
		
		} catch (UnknownHostException e) {
            System.err.println("Don't know about host " + hostName);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " +
                hostName);
            System.exit(1);
        } 
	}

}