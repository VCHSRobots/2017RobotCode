package org.usfirst.frc4415.SteamShipBot1Final;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import com.kauailabs.navx.frc.AHRS;

import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

@SuppressWarnings("unused")
public class TargetReader extends Thread {
	
	private String m_hostName;
	private int m_portNumber;
	private AHRS m_navX;
	private String m_CurrentRequest = "Nothing";
	private String m_PendingRequest = null;
	private int m_nRestarts = 0;
	private int m_nReceived = 0;
	private static Lock m_RequestLock = new ReentrantLock();
	
	public TargetReader(String hostName, int portNumber, AHRS navX){
		this.m_hostName = hostName;
		this.m_portNumber = portNumber;
		this.m_navX = navX;
		this.setName("Target Comm Thread");
	}
	
	public void SetTargetRequest(String request) {
		m_RequestLock.lock();
		m_PendingRequest = request;
		m_RequestLock.unlock();
	}
	
	public int getNumRestarts() {
		return m_nRestarts;
	}
	
	public int getNumReports() {
		return m_nReceived;
	}
	
	private void sleep(int ms) {
		try{
			Thread.sleep(ms);
		} catch (InterruptedException e){
			threadMessage("Target Reader: Interrupted exception caught at sleep in TargetReader.");
		}
	}
	
	public void run(){			
		while(true){
			m_nRestarts++;
			System.out.printf("Target Reader: Restarting TargetReader Comm Loop.  Restart number: %d\n", m_nRestarts);
			restart:
			while(true){
				// wait here till we have a valid request... 
				while (true) {
					m_RequestLock.lock();
					m_CurrentRequest = m_PendingRequest;
					m_RequestLock.unlock();
					if(m_CurrentRequest != null) break;
					sleep(100);
				}
				// Start the main comm loop here...
				try (
					Socket clientSocket = new Socket(m_hostName, m_portNumber);
					PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
				    BufferedReader in = new BufferedReader(
				    		new InputStreamReader(clientSocket.getInputStream()));
				    BufferedReader stdIn = new BufferedReader(
				                    new InputStreamReader(System.in))
				){
					clientSocket.setSoTimeout(2000);
					out.println(m_CurrentRequest);  // Send the command once for this connection!
					while(true) {
						m_RequestLock.lock();
						if (m_CurrentRequest != m_PendingRequest) {
							m_RequestLock.unlock();
							// Start a new connection since we need a different target
							break restart;
						}
						m_RequestLock.unlock();
						String result;
						result = in.readLine();
						if (result == null) {
							System.out.println("Target Reader: Failed to get Targeting data.  Null returned.  Restarting.");
							break restart;
						}
						m_nReceived++;
						if (m_nReceived % 500 == 0) {
							System.out.printf("Target Reader: Number of Target Reports Received = %d\n",  m_nReceived);
							System.out.printf("Target Reader: Sample Target Report = %s\n",  result);
						}
						//System.out.println("Target Result = " + result);
						if (m_CurrentRequest == "T0") {
							sleep(100);  // We don't need the data, cycle slow.
						}
						else {
							sleep(50);  // We NEED the data, cycle faster than they can send it.
						}
					}
				}
				catch (SocketException e){
						System.out.println("Target Reader: Socket Exception in Target Reader Comm Loop.  Restarting in 200ms.");
						sleep(200);
				}
				catch (UnknownHostException e) {
		            System.err.println("Target Reader: Don't know about host " + m_hostName + " In Target Reader Comm Loop.  Exiting for good.");
		            return;
		        } catch (IOException e) {
		            threadMessage("Target Reader: Couldn't get IO connection to " + m_hostName + ".  Retrying in 200ms...");
		            sleep(200);
		        } 	
			}
		}
	}
	
	public static void threadMessage(String message){
		
		// this method displays the name of the thread, followed by the message
		
		String threadName = Thread.currentThread().getName();
		System.out.format("%s: %s%n", threadName, message);
	}
}
