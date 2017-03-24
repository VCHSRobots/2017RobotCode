/*
 * TimeDelay.java
 * 
 * Created 3/23/2017 - KJF
*/
package org.usfirst.frc4415.SteamShipBot1Final;

public class TimeDelay extends GeneralController {
	private long millis=0;
	private long startTime = 0;
	private boolean init=false;
	private boolean done=false;
	public TimeDelay(long millis){
		this.millis = millis;
	}
	
	// this method requires a double to work, which
	// i just throw away.  This is ugly, but 
	// competition starts in 12 hours.
	public void run(double nothing){
		if(!init){
			startTime = System.currentTimeMillis();
			init = true;
		}
	}
	public boolean isDone(){
		if(System.currentTimeMillis()-startTime >= millis){
			done = true;
		}
		return done;
	}
	public String toString(){
		return String.format("Wait    || Set: %d Current: %5d", millis, System.currentTimeMillis()-startTime);
	}
}