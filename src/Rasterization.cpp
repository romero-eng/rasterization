# if defined(__linux__)

# include "Rasterization.hpp" 


std::vector<std::array<int, 2>> Rasterization::Line(const std::array<std::array<int, 2>, 2>& line_points)
{
    const auto& [p_1, p_2] = line_points;
    const auto& [x_1, y_1] = p_1;
    const auto& [x_2, y_2] = p_2;

    int delta_x {x_2 - x_1};
    int delta_y {y_2 - y_1};

    bool non_steep {std::abs(delta_x) > std::abs(delta_y)};

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


# else
# error "This file is only meant to be compiled on a Linux OS"
# endif
