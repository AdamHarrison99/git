package edu.du.cs.aharrison.painter;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.*;

public class Painter1 extends JFrame implements ActionListener {
	boolean lineMode = false;
	boolean circleMode = true;
	Color colorSelection = Color.red;
	Point startPoint, stopPoint;
	private PaintingPanel paintHolder;
	static ObjectOutputStream oosO;
	static ObjectInputStream oisO;
	static Object obj;
	static Socket s;
	static String name;
	static StringBuilder send;
	static JTextField tx;
    static JTextArea ta;
    
	public Painter1()  {
	    
		setSize(500, 500);
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		
		this.setName(name);
		JPanel holder = new JPanel();
		holder.setLayout(new BorderLayout());
		
		JPanel chat = new JPanel();
		JPanel text = new JPanel();
		JPanel shapeHolder = new JPanel();
		JPanel colorHolder = new JPanel();
		paintHolder = new PaintingPanel();
		
		chat.setLayout(new BorderLayout());
		text.setLayout(new BorderLayout());
		shapeHolder.setLayout(new GridLayout(1,2));
		
		ta = new JTextArea();
		chat.add(ta);
		
		tx = new JTextField();
		text.add(tx, BorderLayout.CENTER);
		text.add(chat, BorderLayout.SOUTH);
		text.setBackground(Color.GRAY);
		
		JButton chatb1=new JButton("Send");
		text.add(chatb1, BorderLayout.EAST); 
		chatb1.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) 
			{
				String send = name+": "+tx.getText() + "\n";      
                tx.setText("");  
                try {
					oosO.writeObject(send);
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		});
		
		JButton line = new JButton("line");
		
		shapeHolder.add(line, BorderLayout.NORTH);
		
		line.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				lineMode = true;
				circleMode = false;
			}
		});
		
		JButton circle = new JButton("circle");
		shapeHolder.add(circle, BorderLayout.NORTH);
		circle.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent e) {
				lineMode = false;
				circleMode = true;
			}	
		});
		
		
		colorHolder.setLayout(new GridLayout(3, 1)); // 3 by 1
		
		JButton redPaint = new JButton();
		redPaint.setBackground(Color.RED);
		redPaint.setOpaque(true);
		redPaint.setBorderPainted(false);
		colorHolder.add(redPaint);  // Added in next open cell in the grid
		
		redPaint.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) 
			{
				colorSelection = Color.RED;
			}
		});
		
		// similar for green and blue
		JButton bluePaint = new JButton();
		bluePaint.setBackground(Color.BLUE);
		bluePaint.setOpaque(true);
		bluePaint.setBorderPainted(false);
		colorHolder.add(bluePaint);
		
		bluePaint.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) 
			{
				colorSelection = Color.BLUE;
			}
		});
		
		JButton greenPaint = new JButton();
		greenPaint.setBackground(Color.GREEN);
		greenPaint.setOpaque(true);
		greenPaint.setBorderPainted(false);
		colorHolder.add(greenPaint);
		
		greenPaint.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) 
			{
				colorSelection = Color.GREEN;
			}
		});
		
		paintHolder.addMouseListener(new MouseListener() {

			@Override
			public void mouseClicked(MouseEvent arg0) {}

			@Override
			public void mouseEntered(MouseEvent arg0) {}

			@Override
			public void mouseExited(MouseEvent arg0) {}

			@Override
			public void mousePressed(MouseEvent arg0) {
				startPoint = arg0.getPoint();
			}

			@Override
			public void mouseReleased(MouseEvent arg0) {
				stopPoint = arg0.getPoint();
				if(circleMode == true) {
					Circle c = new Circle(colorSelection, startPoint, stopPoint);
					//paintHolder.addPrimitive(c);
					//System.out.println("Circle");
					try {
						oosO.writeObject(c);
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
				else if(lineMode == true) {
					Line l = new Line(colorSelection, startPoint, stopPoint);
					//paintHolder.addPrimitive(l);
					//System.out.println("line");
					try {
						oosO.writeObject(l);
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
				
			}
			
		});
		
		holder.add(text, BorderLayout.SOUTH);
		holder.add(shapeHolder, BorderLayout.NORTH);
		holder.add(colorHolder, BorderLayout.WEST);
		holder.add(paintHolder, BorderLayout.CENTER);
		
		name = JOptionPane.showInputDialog("Enter your name");
		
		setContentPane(holder);
		setVisible(true);
	
	}

	@Override
	public void actionPerformed(ActionEvent e) {}
	
	public static void main(String[] args) {
		try {
			System.out.println("Looking for Hub");
			s = new Socket("localhost", 7000);
			System.out.println("Connected at " + s);
			oisO = new ObjectInputStream(s.getInputStream());
			oosO = new ObjectOutputStream(s.getOutputStream());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		Painter1 paint = new Painter1();
		
		while(true) {
		try {
			obj = oisO.readObject();
			if(obj instanceof PaintingPrimitive)
				paint.paintHolder.addPrimitive((PaintingPrimitive) obj);
			
			/*else if (obj instanceof String)
				ta.append((String)obj);
				System.out.println((String)obj);*/
		} catch (ClassNotFoundException | IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
}

}
