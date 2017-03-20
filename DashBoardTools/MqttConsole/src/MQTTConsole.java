import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttTopic;


public class MQTTConsole implements MqttCallback {
	private MqttClient myClient = null;
	private MqttConnectOptions connOpt;
	private String BROKER_URL = "tcp://10.44.15.19:5802";
	private String M2MIO_THING = "JavaLaptop";
	private long starttime = 0;

	public static void main(String[] args){
		MQTTConsole app = new MQTTConsole();
		app.runClient();
	}
	
//	public void runit() {
//		//m_client = TryToConnect();
//		//if (m_client == null) return;
//		//m_client.subscribe("robot/jetson/ping");
//		//m_client.setCallback(callback);
//		//while(true) {
//	//	}
//	}

	@Override
	public void connectionLost(Throwable t) {
		System.out.println("Connection lost!");
		System.exit(-1);
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		try {
			System.out.println("Pubishing complete: " + new String(token.getMessage().getPayload()));
		} catch (MqttException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
		long elptime = System.currentTimeMillis() - starttime;
		System.out.printf("Ping Time = %d\n", elptime);
		System.out.println("|-------------------------------------------------");
		System.out.println("| Topic:" + topic);
		System.out.println("| Message: " + new String(message.getPayload()));
		System.out.println("|-------------------------------------------------");
	}

	public void runClient() {
		// setup MQTT Client
		String clientID = M2MIO_THING;
		connOpt = new MqttConnectOptions();
		
		connOpt.setCleanSession(true);
		connOpt.setKeepAliveInterval(30);

		// Connect to Broker
		try {
			myClient = new MqttClient(BROKER_URL, clientID);
			myClient.setCallback(this);
			myClient.connect(connOpt);
		} catch (MqttException e) {
			e.printStackTrace();
			System.exit(-1);
		}
		
		System.out.println("Connected to " + BROKER_URL);

		try {
			int subQoS = 0;
			myClient.subscribe("robot/Jetson/javapingresponse", subQoS);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		MqttTopic topic = myClient.getTopic("robot/JavaLaptop/ping");

		for (int i=1; i<=10; i++) {
	   		String pubMsg = String.format("ping number %2d",  i);
	   		int pubQoS = 0;
			MqttMessage message = new MqttMessage(pubMsg.getBytes());
	    	message.setQos(pubQoS);
	    	message.setRetained(false);

	    	// Publish the message
	    	System.out.println("Publishing to topic \"" + topic + "\" qos " + pubQoS);
	    	IMqttDeliveryToken token = null;
	    	try {
	    		// publish message to broker
	    		starttime = System.currentTimeMillis();
				token = topic.publish(message);
		    	// Wait until the message has been delivered to the broker
				token.waitForCompletion();
				Thread.sleep(1000);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}			

		// disconnect
		try {
			// wait to ensure subscribed messages are delivered
			Thread.sleep(1000);
			myClient.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

//public class MQTTConsole implements MqttCallback {
//	MqttClient m_client = null;
//	
//	public static void main(String[] args){
//		MQTTConsole app = new MQTTConsole();
//		app.runit();
//	}
//	
//	public void runit() {
//		m_client = TryToConnect();
//		if (m_client == null) return;
//		//m_client.subscribe("robot/jetson/ping");
//		//m_client.setCallback(callback);
//		while(true) {
//		}
//		
//	}
//
//	@Override
//	public void connectionLost(Throwable t) {
//	}
//	
//
//	@Override
//	public void deliveryComplete(MqttDeliveryToken token) {
//		//System.out.println("Pub complete" + new String(token.getMessage().getPayload()));
//	}
//	
//	@Override
//	public void messageArrived(MqttTopic topic, MqttMessage message) throws Exception {
//	}
//	
//	// Writes a message to the console -- prepending it with the name of the thread
//	public static void threadMessage(String message){
//		String threadName = Thread.currentThread().getName();
//		System.out.format("%s: %s%n", threadName, message);
//	}
//	
//	private MqttClient TryToConnect()
//	{
//		MqttClient client = null;
//		try {
//			MemoryPersistence persistence = new MemoryPersistence();
//			String url = String.format("tcp://%s:%d", "10.44.15.19", 5802);
//	        client = new MqttClient(url, "RoboRIO", persistence);
//	        MqttConnectOptions connOpts = new MqttConnectOptions();
//	        connOpts.setCleanSession(true);
//	        client.connect(connOpts);
//	        threadMessage("MQTT: connected.");
//	        return client;
//	      }
//		catch (MqttException me) {
//	       	threadMessage(String.format("MQTT: Error in Mqtt startup. Reason/msg = %s, %s", me.getReasonCode(), me.getMessage()));
//	       	return null;
//		}
//	}
//}

//public class Mqtt extends Thread {
//	
//	private String m_hostName;
//	private int m_portNumber;
//	private MqttClient m_client;
//
//	public Mqtt(String hostName, int portNumber) {
//		this.m_hostName = hostName;
//		this.m_portNumber = portNumber;
//		this.setName("MQTT");
//	}
//
//	// This is the main background tread for mqtt.  It keeps checking to
//	// make sure a connection is alive.
//	public void run() {
//		while(true) {
//			while (m_client == null) {
//				sleep(100);
//				m_client = makeConnection();
//			}
//			while (m_client != null && m_client.isConnected()) {
//				sleep(100);
//			}
//		}
//	}
//	
//	private MqttClient makeConnection() {
//
//	}
//	
//
//	
//	// Does a safe sleep for the given number of milliseconds
//	private void sleep(int ms){
//		try{
//			Thread.sleep(ms);
//		} 	catch (InterruptedException e){
//			threadMessage("MQTT: Thread interrupted at connection attempt.");
//		}
//	}
//	
//
//	
//	public boolean SendMessage(String topic, String msg) {
//		return false;
//	}
//	
//	
//}
//
// 		
//		
//			if (m_client == null) {
//				threadMessage("MQTT: No client -- cannot run.");
//				return;
//			}
//		int counter = 0;
//		while (true) {	
//			try {
//				String content = String.format("%d",  counter);
//				MqttMessage msg = new MqttMessage(content.getBytes());
//				m_client.publish("robot/roborio/counter", msg);
//			}
//			catch(MqttException me) {
//		       	threadMessage(String.format("MQTT: Error in Mqtt publishing. Reason/msg = %s, %s", me.getReasonCode(), me.getMessage()));
//		       	return;
//		    }		
//			sleep(2000);
//			counter++;
//		}
//	}
//}
//	