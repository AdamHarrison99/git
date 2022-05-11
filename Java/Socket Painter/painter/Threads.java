package edu.du.cs.aharrison.painter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.ArrayList;

public class Threads extends Hub implements Runnable{
	ArrayList<ObjectOutputStream> ossList;
	Socket s;
	Object obj;
	String string;
	String chat;
	
	Threads(ArrayList<ObjectOutputStream> ossList, Socket s){
		this.ossList = ossList;
		this.s = s;
	}
	
	@Override
	public void run() {
		
		ObjectInputStream ois = null;
		try {
			ois = new ObjectInputStream(s.getInputStream());
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		while(true) {
			if(s.isClosed()) {
				try {
					s.close();
					return;
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
			System.out.println("Waiting for input from my painter");
			try {
				obj = ois.readObject();
				if(obj instanceof PaintingPrimitive) {
					for(int i=0; i<ossList.size(); i++) {
						sendObj((PaintingPrimitive)obj);
					}
				}
				/*else if (obj instanceof String) {
					sendString(string);
				}*/
			} catch (ClassNotFoundException | IOException e) {
				e.printStackTrace();
			}
			System.out.println("Sent input to all painters");
		}
	}
}

