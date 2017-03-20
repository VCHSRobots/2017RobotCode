/*-------------------------------------------------------
 * 
 * PIDController - an object for closed-loop control of 
 * 					an actuator based on a feedback 
 * 					device.
 * 
 * Created by Kyle Fleming, 3/18/2017
 * 
 * Requirements: 
 * 		1. The feedback device MUST go in the 
 * 			same direction as the actuator.
 * 			i.e. if a motor controller is given
 * 			a positive setpoint, the encoder
 * 			should count in the positive direction
 * 		2. For integral control, the actuator must 
 * 			cross the setpoint.
 * 			
 * 
 * Directions: 
 * 		1. To determine the deadband, manually
 * 			increase the value given to the actuator
 * 			until the devices physically begins 
 * 			moving.  Set the deadband to this value.
 * 		2. Set the actuator to a positive value.  
 * 			Check that the feedback device is changing
 * 			in the positive direction.  If not, correct.
 * 
 *///----------------------------------------------------

package org.usfirst.frc4415.SteamShipBot1Final;

public class PIDController {
	
	/*
	 * Tune these values to make controller work.
	 * These values MUST be positive.
	 * See below wikipedia for an understanding 
	 * of PID controllers and some basic tuning 
	 * methods.
	 * 
	 * https://en.wikipedia.org/wiki/PID_controller
	 * 
	 */
	private double pGain = 0;
	private double iGain = 0;
	private double dGain = 0;
	private double clipping = 9999999;
	private double deadband = 0;
	
	/*
	 * The PID loop ends under either of the following 
	 * conditions:
	 * 		1. the feedback is within the range 
	 * 		[setpoint-threshold, setpoint+threshold]
	 * 		for thresholdLoop number of loops
	 * 		2. the time since start of the loop
	 * 		exceed timeout (in milliseconds)
	 */
	private double setpoint = 0;
	private double threshold = 0;
	private int thresholdLoop = 20;
	private long timeout = 10000;
	
	/*
	 * The following variables are internal 
	 * controller variables and should not 
	 * require any changes by the user
	 */
	private double actuator = 0;
	private double pTerm = 0;
	private double iTerm = 0;
	private double dTerm = 0;
	private double deadbandTerm = 0;
	private boolean isInitiated = false;
	private long startTime = 0;
	private long previousTime = 0;
	private long currentTime = 0;
	private boolean directionIsPositive = false;
	private double startPosition = 0;
	private double currentPosition = 0;
	private double previousPosition = 0;
	private int thresholdLoopCounter = 0;
	private boolean done = false;
	private boolean accumulatorEnable = false;
	private double accumulator = 0;	
	private boolean isRelative = false;
	
	public PIDController(double setpoint, 
			boolean isRelative, 
			double threshold, 
			long timeout){
		this.setpoint = setpoint;
		this.isRelative = isRelative;
		this.threshold = threshold;
		this.timeout = timeout;
	}
	
	// Calculates and returns actuator value
	public double calculateActuatorValue
	(double newCurrentPosition){
		currentTime = System.currentTimeMillis();
		// Only runs in the first loop.
		if(!isInitiated){
			startTime = currentTime;
			previousTime = currentTime;
			startPosition = newCurrentPosition;
			previousPosition = startPosition;
			if(setpoint > currentPosition) 
				directionIsPositive = true;
			isInitiated = true;
		}
		if(isRelative) currentPosition = 
				newCurrentPosition - startPosition;
		else currentPosition = newCurrentPosition;
		
		// Calculate the deadband term
		double deadbandSign = -1;
		if(setpoint > currentPosition) deadbandSign = 1;
		deadbandTerm = deadbandSign * deadband;
		
		// Calculate the proportional term
		pTerm = pGain * 
				(setpoint - currentPosition);
		
		/* Calculate the integral term.
		 * First, check if the actuator has passed the 
		 * setpoint.  If so, enable the accumulator.
		 */
		if((directionIsPositive && currentPosition >= 
				setpoint) || (!directionIsPositive && 
				currentPosition <= setpoint)) 
			accumulatorEnable = true;
		if(accumulatorEnable){
			accumulator += setpoint - currentPosition;
		}
		iTerm = iGain * accumulator;
		
		// Calculate the derivative term
		long elapsedTime = currentTime - previousTime;
		double changeInPosition = previousPosition - 
				currentPosition;
		dTerm = dGain * changeInPosition / 
				((double) elapsedTime);
		
		/*
		 * Calculate new actuator value and
		 * clip it if out of range (too big or small)
		 */
		actuator = deadbandTerm + pTerm + iTerm + dTerm;
		actuator = Math.max(clipping * -1, 
				Math.min(clipping, actuator));
		
		// Check end conditions
		if(Math.abs(setpoint - currentPosition) < 
				threshold) thresholdLoopCounter++;
		else thresholdLoopCounter = 0;
		if (thresholdLoopCounter > thresholdLoop ||
				currentTime - startTime > timeout)
			done = true;
		
		// save previous states for next loop
		previousPosition = currentPosition;
		previousTime = currentTime;
		
		return actuator;
	}
	
	public boolean isDone(){
		return done;
	}
	
	public String toString(){
		String s = String.format(
				"Set: %7.3f  " +
				"Current: %7.3f  " +
				"Actuator: %3.3f  " +
				"P: %3.3f  " + 
				"I: %3.3f  " + 
				"D: %3.3f  " + 
				"Dead: %3.3f  ",
				setpoint, currentPosition, actuator,
				pTerm, iTerm, dTerm, deadbandTerm
				);
		
		return s;
		
	}
	
	public void setPGain(double pGain){
		this.pGain = pGain;
	}
	
	public void setIGain(double iGain){
		this.iGain = iGain;
	}
	
	public void setDGain(double dGain){
		this.dGain = dGain;
	}
	
	public double getPTerm(){
		return pTerm;
	}
	
	public double getITerm(){
		return iTerm;
	}
	
	public double getDTerm(){
		return dTerm;
	}
	
	public double getDeadbandTerm(){
		return deadbandTerm;
	}
	
	public void setClipping(double clipping){
		this.clipping = clipping;
	}
	
	public void setDeadband(double deadband){
		this.deadband = deadband;
	}
	
	public void setSetpoint(double setpoint){
		this.setpoint = setpoint;
	}
	
	public void setThreshold(double threshold){
		this.threshold = threshold;
	}
	
	public void setThresholdLoop(int thresholdLoop){
		this.thresholdLoop = thresholdLoop;
	}
	
	public void setTimeout(long timeout){
		this.timeout = timeout;
	}	
	
	public double getActuatorValue(){
		return actuator;
	}

	public void run(double feedback){
		System.out.println("running parent class "
				+ "method instead of child class");
	}
}