import imp
from Transcription.process_transcript import find_sentence_for_frame
from reportlab.rl_config import defaultPageSize
from report_gen import  report_gen

def combine_summaries(sentences,chunks,fr,t_chunk):
    scale = (16/fr)
    chunk_summary = {}
    chunks = sorted(chunks)
    for i in range(len(chunks)-1):
        start_time = chunks[i]*scale
        end_time = (chunks[i+1])*scale
        chunk_summary[chunks[i]] = find_sentence_for_frame(start_time,end_time,sentences)
        s = list(chunk_summary.keys())[0]
        e = list(chunk_summary.keys())[-1]
    if chunks[0]!=0:
        start_time = 0
        end_time = (chunks[0])*scale
        chunk_summary[s]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[s]}
    if chunks[-1]!=t_chunk:
        start_time = chunks[-1]*scale
        end_time = (t_chunk)*scale
        chunk_summary[e]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[e]}
    return chunk_summary

if __name__=="__main__":
    ip = r'E:\Multi-Modal Summarization\Data\videos\Lecture 30-20211028 0641-1.mp4'
    PAGE_WIDTH = defaultPageSize[0]
    sentences ={
  "61.0": "So if the words are nearby in the Iraqi organization, the thesaurus, we say they are similar.",
  "72.0": "And if they are very far apart in the R key, they might be different.",
  "78.5": " So the idea of finding the similarity using the knowledge based approach would be to find out the distances between the two words.",
  "85.0": "And if you find out that the distance between the two words is minimum or smaller than we could predict that they are most similar.",
  "95.0": " And when we say the two words are near nearby in the hierarchical organization, in the sense we are trying to find out, the distances between the two words, and in other terminology also we are trying to find out the similarity between the two words.",
  "129.33333333333334": " They are nearby.",
  "134.66666666666669": " Logically we say that they are similar to each other and if they are far apart, then much dissimilar.",
  "140.0": "So.",
  "142.0": "We use this idea to find out the similarity distance idea, find out the similarity between the two words.",
  "150.0": "No more for finding out the similarity using the knowledge base.",
  "193.0": "Finding out the similarity between 2 words right so is area height or the glasses definitions.",
  "202.5": " Are the two types of approaches you would find in practice being used for finding out the similarity between 2 words.",
  "212.0": "No.",
  "214.0": "Semantic similarity between words and word relatedness.",
  "219.0": "Now what do we understand by semantic similarity or relatedness? We call semantic similarity or relatedness as the degree to which two concepts are related.",
  "258.6666666666667": " But they are not similar.",
  "268.0": "So I said similarity measures are limited to this error key OK, whereas if you look into relatedness measures can be applied to all kinds of relations.",
  "275.5": " So when we go, we're talking for finding out the semantic similarity between 2 words.",
  "283.0": " So typically we go for using the right the hypernymy hierarchy to find out the semantic similarity between 2 words.",
  "290.5": " But when we talk about relatedness, it can be applied to all.",
  "298.0": "Find soft relations, not typically hypernym.",
  "302.0": "Some examples of related words is like car gasoline.",
  "341.0": " Path based similarity measure.",
  "345.0": "So the basic idea in part dissimilarity measure is.",
  "351.0": "We are trying to find out the path between 2 words in the hypernymy graph.",
  "360.0": "So we say 2 words are similar if they are nearby in the hypernymy graph, we are just trying to find out the parts between the two worlds in the hypernymy graph.",
  "369.6666666666667": " OK, so we usually say that 2 words are similar if they are nearby in the hypernymy graph towards a similar.",
  "462.0": "Similarity is nothing but.",
  "466.0": "Closely proportional to similarity between the two and Sept, C1, and C2, using the path based measure is equal to 1 up on one plus part.",
  "478.0": "Of the two concepts C1 and C2, so similarity is inversely proportional to park leg.",
  "488.0": "So.",
  "490.0": "How do we go for finding out the similarity between words using the pathlength based measure?",
  "569.6000000000001": " Then what I'm going to do? I'm going to find out the similarity between the sense one of word one with every sense of word two.",
  "575.8000000000002": " So I'm going to find out similarity of South one one with two, One South, one one with two two South, one with two three similarly South 1-2 with South 22 S 1-2 with.",
  "582.0": "2112 with S23 and so forth.",
  "586.8333333333334": " OK, so we are trying to find out the similarity between every sense of first word with every sense of other word.",
  "591.6666666666667": " And then you will be picking that particular combination which is giving a maximum similarity value.",
  "765.0": " This is another way of estimating it, but if you are given this typical hypernymy graph directly, looking at this hypernymy graph currently because because we don't know how many sensors every word is having.",
  "773.0": " So let us look at the hypernymy graph and with respect to the graph, let us go for finding of the shortest.",
  "781.0": "Pot.",
  "783.0": "Between any two concepts which will help us to find out the similarity using pathways measure.",
  "788.5": " So let us look at Nikhil and money.",
  "828.4000000000001": " It's .",
  "832.6000000000001": "5, right? Similarly, somewhere you go bottom up the air arkie and nickel and coin you have found it to be .",
  "836.8000000000002": "5.",
  "841.0": "Ah.",
  "844.0": "So that's the way we are finding it.",
  "847.0": "The similarity between two concepts or two words using the path based measure.",
  "857.0": "No.",
  "1093.0": "Is 1 but I have taken into consideration the path length we have found out by the Sparc based measure.",
  "1103.0": "OK, so like then while I found it as .",
  "1106.5": "5 so.",
  "1110.0": "I am thinking this is .",
  "1111.5": "5.",
  "1113.0": "So do not get confused with that also right?",
  "1150.3333333333335": " So you can take it as part length between the two as one.",
  "1153.0": "Similarly, entity abstraction that is entity and that is abstraction.",
  "1159.0": "Ogier",
  "1160.0": "the beginning one.",
  "1162.0": "So again, it would be minus log of 1 by 20 whatever value you get OK.",
  "1176.5": " The similarity found out by LC measure would be the same.",
  "1183.0": "For nickel and coin for entity and abstraction, it is minus log of 1 by 20 or nickel and coin minus log 1 by 24 entity extraction.",
  "1194.0": "OK.",
  "1196.0": "No.",
  "1199.0": "As I was talking also when we were talking about part by similarity measure, there are problems.",
  "1295.0": "5 similarity between ND and entity and abstraction is .",
  "1301.0": "5.",
  "1307.0": "This this nickel in coin is with respect to you.",
  "1312.0": " I think part based yes, entity and abstraction is with respect to past base and if you look at LC measure or nickel and coin you are getting it as .",
  "1317.0": "3979 and also for entity abstraction you're getting .",
  "1337.0": "Dog won by 20 but.",
  "1341.0": "Whatever value we get it, but both this value would be the same value, OK?",
  "1346.0": "So as we are going down into the hierarchy, we are moving to very, very specific concepts while we are moving this specific concepts, the same path length should amount to a higher similar similarity value then it is doing in the.",
  "1362.0": "A year labels.",
  "1366.0": "But we are more interested in finding out the matrix which assigns different weightages OK two.",
  "1376.0": "Or different lens or different weight values to the edges which are at a higher level and to the edges which at a deeper level.",
  "1387.0": "So we want a matrix that represents the cost of each edge independently.",
  "1393.0": "And the words connected only through abstract nodes.",
  "1405.5": " So we want the matrix to give us any information where the nodes at a generic label, the cost of every edge between the two concepts, should be different as compared to cost of the edges are deeper level.",
  "1418.0": "So the idea is we use the concept probability model.",
  "1471.0": "So every ward is represented as an entity, so every concept is represented as an entity.",
  "1478.5": " So for each concept we go for finding out the viability of the concept.",
  "1486.0": "Right?",
  "1487.0": "So when we talk about concept probability model, we are treating every concept or every word as an entity and then we go for finding out the probability for that concept.",
  "1498.0": "And how do we go for doing it? How do we go for finding find initially the count for every concept which will help to find out the probability for that concept.",
  "1509.0": "So the idea is whatever.",
  "1514.0": "VC.",
  "1516.0": "As I said.",
  "1518.0": "Is an entity.",
  "1630.0": " At this point of time will have a value of 1 and you will add 1 to entity.",
  "1634.0": " Then you have measure.",
  "1638.0": " Measure will have a count of 1, but all the concepts on the path from root to your dare count will be incremented by one.",
  "1642.0": " So will you will add 1 to abstraction 1 to entity.",
  "1646.0": "That you have standard the moment you have standard it will have a count of 1.",
  "1667.0": "OK.",
  "1669.0": "So by this what will happen?",
  "1676.0": "You get a concept.",
  "1678.0": " County of this form.",
  "1680.0": "At the moment you look at entity, you should immediately understand that these are the.",
  "1698.5": " Total number of concepts existing in this.",
  "1708.0": "Tree.",
  "1710.0": "Goodnight, then immediately we can understand how we can go for finding out the liability.",
  "1717.0": "So again, to give you an example, each occurrence of dying.",
  "1725.0": "And so increments the count for coinage.",
  "1915.0": "So you could find out.",
  "1918.0": "The.",
  "1920.0": "Probability of entity is nothing but entity count on and where capital N is the concept count of the root node, which is 1915712.",
  "1930.0": "So that's why we have the probability of entity as one probability of abstraction is out of step count of extraction extraction divided by N, which comes out to be 5.",
  "1938.0": "51 point 551.",
  "1955.0": "And once we have the concept probability, what we are saying that the nodes higher in the hierarchy would be having higher probabilities as compared to the nodes or the concepts or the words lower in the dark.",
  "1969.0": "Now how this idea will help us to find out the similarity between 2 concepts?",
  "1977.0": "So if.",
  "1978.0": "Probability of a concept is very high than it does not contain much information.",
  "1989.0": "OK, so if probability of a concept is very high then it is not containing much information and if probability for concept is low then it contains some information or more information.",
  "2003.0": "So we say that the probabilities of concepts with very high value do not have much information.",
  "2011.0": "But probability of concept is low implies it contains more information.",
  "2019.0": "So information contents is a measure which measures the specificity of a concept.",
  "2025.0": " So if if.",
  "2031.0": "You are trying to measure the specificity using the information content then.",
  "2071.0": "More appropriately, for specific nodes and generic nodes, so you can look at.",
  "2079.0": "Minus log of probability of a concept.",
  "2086.5": " So the concepts which are up in there are key will be having less information content value as compared to concepts which are more deeper into the tree, more specific.",
  "2094.0": "OK.",
  "2096.0": "So remember this formulation.",
  "2100.0": " We have to find out the information of every node.",
  "2104.0": "So the nodes which are deeper into the tree are said to contain more information content as compared to the nodes which are higher in the R key.",
  "2113.0": "OK.",
  "2116.0": "No.",
  "2117.0": "What is lowest common sub zoomer?",
  "2120.0": "We write it as LCS of two concepts.",
  "2125.6666666666665": " Always subsume is found with respect to some concepts, at least two.",
  "2172.0": "We apply this formulation on every node.",
  "2176.0": "This is the information content value we are getting.",
  "2180.25": " We are slowly minus log of probability of the concept.",
  "2184.5": " So root is having the ability of 1.",
  "2188.75": " So obviously by this formulation entity will be having information, content is 0.",
  "2193.0": "Extraction by .",
  "2195.5": "596 measured as 2.",
  "2198.0": "691.",
  "2200.5": " Used if you start looking deeper into the tree.",
  "2203.0": "Having more information content as compared to the nodes at higher level.",
  "2209.0": "OK.",
  "2235.0": "So the most informative you know in the hierarchy subsuming the concept C1 and C2 would be called as lowest common subsume.",
  "2239.3333333333335": " So let us take an example with respect to the CR Key tree.",
  "2243.666666666667": " What we can see.",
  "2248.0": "What are the sub zoomers of hill and rich?",
  "2251.0": "Summers of Hill and Richard the common anxious tears of both of them.",
  "2330.0": "It depends on how much they have in common.",
  "2333.0": "So the snake similarity measures the commonality by the information content of the lowest common subsume.",
  "2346.0": "So what we are saying that in Resnik similarity we are measuring the similarity between the two words by measuring how much common they have.",
  "2357.0": "OK, we are measuring the commonality between the two concepts, and the commonality is measured with reference to the information content of the lowest common sub servers.",
  "2369.0": "So the Resnik similarity between 2 concepts CC-1 and C2 is found out as information content of the lowest common sub zoomer of seven seat.",
  "2426.0": "Let's look at nickel and coin and we will look at entity and abstraction.",
  "2432.0": "So what would be the?",
  "2435.0": "Similarity between nickel and coil using Resnik similarity.",
  "2440.0": "What does Reznik telling us it is information content of lowest common Subs Umarov, nickel and coin?",
  "2448.0": "Now what is this?",
  "2451.0": "This is.",
  "2453.0": "By ability value.",
  "2606.0": "The concepts nickel and coin.",
  "2609.0": "If you look at the nickel and dime.",
  "2612.0": "Oh yeah, So what is the lowest common subsume of nickel and dime coin right now? What is the similarity between nickel and coin? Using this reasoning similarity, it is also 7.",
  "2620.0": "455.",
  "2628.0": "Right, if you look at nickel and money, the least common subsume of nickel and money is medium of exchange.",
  "2730.0": "Was the same.",
  "2733.0": "Coinage and money.",
  "2737.0": "And.",
  "2739.0": "What I have taken.",
  "2741.0": "Klein agent budget.",
  "2751.0": "Or in other words.",
  "2753.0": "A year from the from the slide itself, what we can see is.",
  "2761.0": "And nickel and dime.",
  "2763.0": "They'd send coin and nickel and dime.",
  "2767.0": "But you could take or.",
  "2770.0": "Nickel and money.",
  "2773.0": "And.",
  "2776.0": "Nickel and budget both are having 6.",
  "2796.0": "Concerts.",
  "2797.0": "Like Google and coin.",
  "2800.0": "Or",
  "2804.0": "other examples for Nick and money, nickel and budget would be the same.",
  "2811.0": "So the Elks, the least common sub zoomer for nickel and money, is medium of exchange and budget.",
  "2817.0": " Is medium of change.",
  "2823.0": " OK, so for both of them, the similarity value would be same.",
  "2829.0": " Why we are getting it same because we are occurring how much information they share, how much information they have in common.",
  "2977.0": "So.",
  "2981.0": "Similarity between let us say coinage and money would be.",
  "2989.0": "The information content common to coinage and money.",
  "2994.0": "Normalized by average information, content of coinage and money.",
  "3000.0": "So that's why we take it as.",
  "3002.6666666666665": " What is the information content of coinage and money? It is 6.",
  "3005.333333333333": "255.",
  "3008.0": "The point of 6.",
  "3010.0": "255 upon.",
  "3012.0": "Information, content of coinage and money.",
  "3016.0": " So, which gives you this is nothing, but we are saying that.",
  "3020.0": "Normalized by average information content which gives us .",
  "3022.5": "8091.",
  "3025.0": "So the similarity between coinage and money bailing similarity.",
  "3027.5": " We get it as .",
  "3030.0": "8091 for coinage and budget.",
  "3032.5": " We get it as .",
  "3035.0": "7012 for nickel and money.",
  "3037.5": " We get it as .",
  "3040.0": "6192 and for nickel and coil we get it as .",
  "3042.5": "7600.",
  "3045.0": "OK.",
  "3050.0": "So putting that similarity on the information content graph, so where we were trying to find out between nickel and coin at this point 670 between nickel and dime, it comes out to be .",
  "3057.75": "607.",
  "3065.5": " Similarly, between nickel and money.",
  "3073.25": " At this point, 619 and between nickel and Richter scale it is 0.",
  "3081.0": "Now even we can go ahead and we can go for using information content to assign lens to graph edges.",
  "3096.0": "So I will talk on this because how much time is remaining? Because I'll need at least 5 minutes.",
  "3099.6666666666665": " Yeah this time, so I'll talk on this.",
  "3103.333333333333": " Yeah, I'll finish it on this.",
  "3107.0": "So.",
  "3117.0": "So we go to finding out JC similarity OK?",
  "3122.0": "And Jesus similarity is found out.",
  "3127.0": "By finding.",
  "3131.0": "No.",
  "3134.0": "By using this formulation.",
  "3136.0": "JC similarity between the concepts C1 and C2 is nothing but one upon information content of C1 plus information content of C2 minus twice information content of least common subsume of C1C2.",
  "3153.0": "And the distance of the concept.",
  "3156.0": "See.",
  "3159.0": "The graph has found out us.",
  "3162.0": "Information content of C minus in information contact the hypernymy of C.",
  "3171.0": "I should say, and C1 and C2.",
  "3278.3333333333335": "163 as information content of money that is 8.",
  "3282.666666666667": "042 minus twice information content of the least common subsume of nickel and money.",
  "3287.0000000000005": " So least common subsume of nickel and money is medium of exchange, so it's minus 2 into 6.",
  "3291.333333333334": "255 right? It comes out to be .",
  "3295.6666666666674": "1.",
  "3300.0": "That's the way you go for finding out is young cornett similarity.",
  "3304.0": " Similarity is nothing but one upon distance measure.",
  "3308.0": "Do you go for finding out distance between nickel and coin? It would be information content of nickel plus information content of coin minus twice information content of least common sub zoomer of nickel and coin."
}
    chunks =   [
    31,
    7,
    114,
    191,
    169,
    263,
    240,
    331,
    354,
    157,
    300,
    482,
    421,
    521,
    854,
    593,
    612,
    727,
    645,
    669,
    780,
    794,
    811,
    856
  ]
    fr= 4
    t_chunk = 858
    report_dic = combine_summaries(sentences,chunks,fr,t_chunk)
    report_gen(report_dic,ip,fr)