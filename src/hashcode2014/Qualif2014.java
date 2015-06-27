package hashcode2014;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by Alex on 3/6/2015.
 */
public class Qualif2014 {

	public static void main(String[] args) {
		System.out.println("Hello, World!");
		new Solver("doodle.txt");
	}
}

public class Solver {
	int rows;
	int cols;
	int i_c; // i current
	int i_m; // i max for the biggest square from the current i. i_m >= i_p >= i_c
	BufferedReader br;
	PrintWriter writer;

	// Updated map that keeps the original can be reverted
	Map<Integer, MapPoint[]> map = new HashMap<>(); // 0, 1, 2: was zero but has square, 3: was one and has square
	Map<Integer, ArrayList<Square>> squareCache_t = new HashMap<>(); //from topLeft of square matching to index line
	Map<Integer, ArrayList<Square>> squareSol_m = new HashMap<>(); //from middle of square matching to index line

	s = {}

	public Solver(String fileName) {
		// init ArrayLists
		for(int i=1;i<=rows;i++) {
			squareCache_t.put(i, new ArrayList<>());
			squareSol_m.put(i, new ArrayList<>());
		}

		try {
			br = new BufferedReader(new FileReader(fileName));
			writer = new PrintWriter("sol_qualif_2014.txt", "UTF-8");
			String[] parameters = br.readLine().split(" ");
			rows = Integer.parseInt(parameters[0]);
			cols = Integer.parseInt(parameters[1]);

			for(i_c = 1; i_c <= rows; i_c++) {
				treatLine();
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void treatLine() {
		MapPoint[] row_c = parseLine(i_c);

		//build new squares
		squareCache_t.put(i_c,  new ArrayList<>());
		i_m = i_c;
		for(int r = 0; r<rows ; r++) {
			if(row_c[r]) {
				i_m = Math.max(i_m, createSquares_c(r, 1, 0));
			}
		}

		// check conflicts
		MapPoint[] row_p;
		for(int i_p = i_c+1; i_p <= i_m; i_p++) {
			row_p = parseLine(i_p);
			for(int r = 0; r<rows ; r++) {
				if(row_p[r]) {
					checkConflictSquares(i_p, r, 1, 0);
				}
			}
		}

		// apply squares
		ArrayList<Square> squaresSol_c = squareSol_m.get(i_c);
		for(Square s_sol : squaresSol_c) {

			writer.println("The first line");
			writer.println("The second line");
			writer.close();
		}
	}

	public int createSquares_c(int r, int size, int prevScore) {
		int score = prevScore + absoluteDiffScore(i_c, r, size);
		ArrayList<Square> squares_t_c = squareCache_t.get(i_c);
		if(score>0) {
			addSquare_c(new Square(i_c, r, size, score));
		}
		if(r+size+2 < rows) {
			return createSquares_c(r, size+2, score);
		} else {
			return i_c + size -1;
		}
	}

	public void checkConflictSquares(int i, int r, int size, int prevScore) {
		int score = prevScore + absoluteDiffScore(i, r, size);

		Square s = new Square(i, r, size, score);
		// dont create if in the cache for this max size ???
		ArrayList<Square> squares_t_c = squareCache_t.get(i_c);

		// remove less good squares
		for(Square s_c : squareCache_t) {
			if(s.touches(s_c)) {
				if(s.absScore > s_c.absScore) {
					removeSquare_c(s_c);
				}
			}
		}

		if (i + (size+2) <= i_m) {
			checkConflictSquares(i, r, size + 2, score);
		}
	}

	public MapPoint[] parseLine(int i) {
		MapPoint[] row = map.get(i);
		if(row != null) {
			return row;
		}

		row = new MapPoint[rows];
		String line;
		try {
			line = br.readLine();
		} catch(IOException e) {
			e.printStackTrace();
			return row;
		}

		for(int r = 0; r<rows ; r++) {
			if(line.charAt(r) == '#') {
				row[r] = new MapPoint(true);
			} else {
				row[r] = new MapPoint(false);
			}
		}
		map.put(i, row);
		return row;
	}

	// add square and update map
	public void addSquare_c(Square s) {
		for(int i = s.i; i < s.i + s.size; i++) {
			byte[] row_i = map.get(i);
			for(int r = s.r; r < s.r + s.size; r++) {
				if(row_i[r] == 0) {
					row_i[r] = 2;
				} else if(row_i[r] == 1) {
					row_i[r] = 3;
				}
			}
			map.replace(i, row_i);
		}
		squareCache_t.get(s.i).add(s);
	}

	public void removeSquare_c(Square s) {
		for(int i = s.i; i < s.i + s.size; i++) {
			MapPoint[] row_i = map.get(i);
			for(int r = s.r; r < s.r + s.size; r++) {
				if(row_i[r].black) {
					row_i[r] = 3;
				} else if(row_i[r] == 1) {
					row_i[r] = 4;
				}
			}
			map.replace(i, row_i);
		}
		squareCache_t.get(s.i).remove(s);
	}


	/**
	 * (i,r) to right and top of size, ony calc the border
	 */
	public int absoluteDiffScore(int i, int r, int size) {
		int score = 0;
		for(int i_l = i; i_l <= i+size ; i_l++) {
			if(map.get(i_l)[r+size] == 0 || map.get(i_l)[r+size] == 2) {
				score++;
			} else {
				score--;
			}
		}
		for(int r_l = r; r_l < r+size ; r_l++) {
			if(map.get(i+size)[r_l] == 0 || map.get(i+size)[r_l] == 2) {
				score++;
			} else {
				score--;
			}
		}
		return score;
	}

	public class Square {
		// (i,r) = top left
		int i;
		int r;
		int size;
		int absScore; // absolute score independent of other Squares

		public Square(int i, int r, int size, int absScore) {
			this.i = i;
			this.r = r;
			this.size = size;
			this.absScore = absScore;
		}

		public boolean isWorth() {

		}
	}

	public class MapPoint {
		public boolean black;
		public int layers; // count layers of squares on it

		MapPoint(boolean black) {
			this.black = black;
		}
		public void addLayer() {
			this.layers++;
		}

		/**
		 * @return was necessary
		 */
		public boolean removeLayer() {
			if(this.layers > 0) {
				this.layers--;
				return true;
			} else {
				return false;
			}
		}
	}
}
//	Array of actions (strings)
//		Number of actions
//
//	ic current line
//	n size of current process
//	im line max that was read
//
//	public void TreatLine() {
//		// Read 2 lines and if there is a block, find block with most dark points covered7
//		returns a list of blocks of this i
//	}
//
//	public void BiggestBlock() {
//		Each new line update the i -> block(s) -> array of blocks that touch
//				and iplus->the blocks of the arrays
//		// Each ne line gives new potential blocks from n-1 init pos
//		// until a line has zero discovery
//	}
//
//	public void count actions(line) {
//		use blocks status to count actions and add them to actions
//	}
//
//	Line.i
//	Line.array of block
//
//	block.x
//	block.y
//	block.size
//	block.array of touching blocks
//			block.status chosen or new

