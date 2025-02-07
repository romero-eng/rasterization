# ifndef RASTERIZATION_H
# define RASTERIZATION_H

# include <cmath>
# include <vector>
# include <array>

namespace Rasterization
{
    std::vector<std::array<int, 2>> Line(const std::array<std::array<int, 2>, 2>& line_points);
}

#endif
