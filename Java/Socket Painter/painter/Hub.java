package edu.du.cs.aharrison.painter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Hub {
	static ArrayList<ObjectOutputStream> ossObjList = new ArrayList<ObjectOutputStream>();
	static ArrayList<PaintingPrimitive> paintObjList = new ArrayList<PaintingPrimitive>();
	
	public static void main(String[] args) {
		try {
			ServerSocket ss = new ServerSocket(7000);
			while(true) {
				System.out.println("Waiting for a Painter");
				Socket s = (ss.accept());
				ObjectOutputStream oosO = new ObjectOutputStream(s.getOutputStream());
				ossObjList.add(oosO);
				addPaintingPrimitives(oosO);
				
				Threads oosT = new Threads(ossObjList, s);
				Thread oosTh = new Thread(oosT);
				oosTh.start();
				
				System.out.println("Added new Painter");
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
	
	static void addPaintingPrimitives(ObjectOutputStream ossO) {
		try {
			for(int i = 0; i < paintObjList.size(); i++) {
				ossO.writeObject(paintObjList.get(i));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	void sendObj(PaintingPrimitive obj) {
			try {
				paintObjList.add(obj);
				for(ObjectOutputStream i : ossObjList) {
					i.writeObject(obj);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
	}
	
	void sendString(String string) {
		try {
			for(ObjectOutputStream i : ossObjList) {
				i.writeObject(string);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
