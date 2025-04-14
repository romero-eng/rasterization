# if defined(__linux__)

# include "Rasterization.hpp" 


std::vector<std::array<int, 2>> Horizontal_Line(const std::array<std::array<int, 2>, 2>& line_points)
{
    const auto& [p_1, p_2] = line_points;
    const auto& [x_1, y_1] = p_1;
    const auto& [x_2, y_2] = p_2;

    int y {y_1};
    int delta_x {x_2 - x_1};
    int sgn_delta_x {delta_x >= 0 ? 1 : -1};
    std::size_t N {static_cast<std::size_t>(std::abs(delta_x))};

    std::vector<std::array<int, 2>> points (N + 1);

    points[0] = {x_1, y};
    points[N] = {x_2, y}; 
    for(std::size_t n {0}; n < N - 1; n++){
        points[n + 1] = {points[n][0] + sgn_delta_x, y}; 
    }

    return points;
}


std::vector<std::array<int, 2>> Vertical_Line(const std::array<std::array<int, 2>, 2>& line_points)
{
    const auto& [p_1, p_2] = line_points;
    const auto& [x_1, y_1] = p_1;
    const auto& [x_2, y_2] = p_2;

    int x {x_1};
    int delta_y {y_2 - y_1};
    int sgn_delta_y {delta_y >= 0 ? 1 : -1};
    std::size_t N {static_cast<std::size_t>(std::abs(delta_y))};

    std::vector<std::array<int, 2>> points (N + 1);

    points[0] = {x, y_1};
    points[N] = {x, y_2};
    for(std::size_t n {0}; n < N - 1; n++){
        points[n + 1] = {x, points[n][1] + sgn_delta_y};
    }

    return points;
}


std::vector<std::array<int, 2>> Diagonal_Line(const std::array<std::array<int, 2>, 2>& line_points)
{
    const auto& [p_1, p_2] = line_points;
    const auto& [x_1, y_1] = p_1;
    const auto& [x_2, y_2] = p_2;

    int delta_x {x_2 - x_1};
    int delta_y {y_2 - y_1};
    int sgn_delta_x {delta_x >= 0 ? 1 : -1};
    int sgn_delta_y {delta_y >= 0 ? 1 : -1};
    std::size_t N {static_cast<std::size_t>(std::abs(delta_x))};

    std::vector<std::array<int, 2>> points (N + 1);

    points[0] = {x_1, y_1};
    points[N] = {x_2, y_2};
    for(std::size_t n {0}; n < N - 1; n++){
        points[n + 1] = 
            {points[n][0] + sgn_delta_x,
             points[n][1] + sgn_delta_y};
    }

    return points;
}


std::vector<std::array<int, 2>> Rasterization::Line(const std::array<std::array<int, 2>, 2>& line_points)
{
    const auto& [p_1, p_2] = line_points;
    const auto& [x_1, y_1] = p_1;
    const auto& [x_2, y_2] = p_2;

    int delta_x {x_2 - x_1};
    int delta_y {y_2 - y_1};

    int abs_delta_x {std::abs(delta_x)};
    int abs_delta_y {std::abs(delta_y)};

    if(delta_x == 0) {
        return Vertical_Line(line_points);
    } else if (delta_y == 0) {
        return Horizontal_Line(line_points);
    } else if (abs_delta_x == abs_delta_y) {
       return Diagonal_Line(line_points); 
    } else {

        bool non_steep {abs_delta_x > abs_delta_y};

        int delta_I {non_steep ? delta_x : delta_y};
        int delta_O {non_steep ? delta_y : delta_x};
        int O_1 {non_steep ? y_1 : x_1};
        int O_2 {non_steep ? y_2 : x_2};
        std::size_t orthogonal_axis {static_cast<std::size_t>(non_steep ? 1: 0)};

        int sgn_delta_x {delta_x >= 0 ? 1 : -1};
        int sgn_delta_y {delta_y >= 0 ? 1 : -1};
        int sgn_delta_O {delta_O >= 0 ? 1 : -1};

        std::size_t N {static_cast<std::size_t>(std::abs(delta_I))};
        int T {static_cast<int>(N) - 2*sgn_delta_O*((static_cast<int>(N) - 1)*O_1 + O_2)};

        std::vector<std::array<int, 2>> points (N + 1);
        points[0] = {x_1, y_1};
        points[N] = {x_2, y_2};

        bool decision;

        for(std::size_t n{0}; n <= N - 2; n++) {
        
            decision = (sgn_delta_O*(static_cast<int>(n)*delta_O - static_cast<int>(N)*points[n][orthogonal_axis]) << 1) >= T;

            points[n + 1] = \
                {points[n][0] + sgn_delta_x*(    non_steep || decision ? 1 : 0),
                 points[n][1] + sgn_delta_y*(not non_steep || decision ? 1 : 0)};
        } 

        return points;
    }
}


// Function only included for testing
void print_pixels(const std::vector<std::array<int, 2>>& points)
{
    std::vector<std::string> points_as_strings (points.size());
    std::transform(points.begin(),
                   points.end(),
                   points_as_strings.begin(),
                   [](const std::array<int, 2>& point){ return fmt::format("({:d}, {:d})",
                                                                           point[0],
                                                                           point[1]); });
    fmt::print("{:s}", fmt::join(points_as_strings, "\n"));
}


int main()
{

    int x_c {0};
    int y_c {0};
    int radius {20};

    std::size_t N {static_cast<std::size_t>(radius/std::sqrt(2)) + 1};
    int tau {4*radius*radius - 5};

    std::vector<std::array<int, 2>> first_octant_points (N);
    first_octant_points[0] = {radius, 0};

    bool decrement;
    for (std::size_t n {0}; n < N - 1; n++) {

        decrement = 4*(first_octant_points[n][0]*first_octant_points[n][0] - first_octant_points[n][0] + static_cast<int>(n*n) + 2*static_cast<int>(n)) >= tau;

        first_octant_points[n + 1] = 
           {first_octant_points[n][0] - (decrement ? 1 : 0),
            first_octant_points[n][1] + 1}; 

    }

    std::size_t overflow {static_cast<std::size_t>(first_octant_points[N - 1][0] == first_octant_points[N - 1][1] ? 1 : 0)};
    std::size_t M {N - overflow};
    std::size_t Q {2*N - 1 - overflow};

    std::vector<std::array<int, 2>> circular_arc_points (4*Q);

    circular_arc_points[0] = \
        {first_octant_points[0][0] + x_c,
         first_octant_points[0][1] + y_c};

    circular_arc_points[Q] = \
        {first_octant_points[0][1] + x_c,
         first_octant_points[0][0] + y_c};

    circular_arc_points[2*Q] = \
        {-first_octant_points[0][0] + x_c,
          first_octant_points[0][1] + y_c};

    circular_arc_points[3*Q] = \
        {-first_octant_points[0][1] + x_c,
         -first_octant_points[0][0] + y_c};

    if (overflow == 1) {
        
        circular_arc_points[N - 1] = \
            {first_octant_points[N - 1][0] + x_c,
             first_octant_points[N - 1][1] + y_c};

        circular_arc_points[2*Q - (N - 1)] = \
            {-first_octant_points[N - 1][0] + x_c,
              first_octant_points[N - 1][1] + y_c};

        circular_arc_points[2*Q + (N - 1)] = \
            {-first_octant_points[N - 1][0] + x_c,
             -first_octant_points[N - 1][1] + y_c};

        circular_arc_points[4*Q - (N - 1)] = \
            { first_octant_points[N - 1][0] + x_c,
             -first_octant_points[N - 1][1] + y_c};

    }

    for (std::size_t m {1}; m < M; m++) {
        
        circular_arc_points[m] = \
            {first_octant_points[m][0] + x_c,
             first_octant_points[m][1] + y_c};

        circular_arc_points[Q - m] = \
            {first_octant_points[m][1] + x_c,
             first_octant_points[m][0] + y_c};

        circular_arc_points[Q + m] = \
            {-first_octant_points[m][1] + x_c,
              first_octant_points[m][0] + y_c};

        circular_arc_points[2*Q - m] = \
            {-first_octant_points[m][0] + x_c,
              first_octant_points[m][1] + y_c};

        circular_arc_points[2*Q + m] = \
            {-first_octant_points[m][0] + x_c,
             -first_octant_points[m][1] + y_c};

        circular_arc_points[3*Q - m] = \
            {-first_octant_points[m][1] + x_c,
             -first_octant_points[m][0] + y_c};

        circular_arc_points[3*Q + m] = \
            { first_octant_points[m][1] + x_c,
             -first_octant_points[m][0] + y_c};

        circular_arc_points[4*Q - m] = \
            { first_octant_points[m][0] + x_c,
             -first_octant_points[m][1] + y_c};

    }

    // print_pixels(first_octant_points);
    print_pixels(circular_arc_points);

    return 0;
}


# else
# error "This file is only meant to be compiled on a Linux OS"
# endif
