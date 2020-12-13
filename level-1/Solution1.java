public class Solution1 {

    public static void main(String[] args) {
        System.out.println(solution("ababab"));
    }

    public static int solution(String sequence) {
        final int sequenceLength = sequence.length();

        for (int i = 1; i < sequenceLength; i++) {
            if (sequenceLength % i == 0) {
                String part = sequence.substring(0, i);
                int occurrences = countOccurrences(sequence, part);
                if (occurrences * part.length() == sequenceLength) {
                    return occurrences;
                }
            }
        }

        return 1;
    }

    // Returns the number of occurrences sub in the string s
    private static int countOccurrences(String s, String sub) {
        return s.split(sub, -1).length - 1;
    }
}
