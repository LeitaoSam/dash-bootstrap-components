import React from 'react';
import PropTypes from 'prop-types';
import {Tooltip as RSTooltip} from 'reactstrap';

class Tooltip extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      tooltipOpen: false
    };
  }

  toggle() {
    this.setState({
      tooltipOpen: !this.state.tooltipOpen
    });
  }

  render() {
    const {
      id,
      children,
      isOpen,
      ...otherProps
    } = this.props;
    return (<RSTooltip toggle={this.toggle} isOpen={this.state.tooltipOpen} {...otherProps}>
      {children}
    </RSTooltip>);
  }
}

Tooltip.propTypes = {
  /**
   * The ID of this component, used to identify dash components
   * in callbacks. The ID needs to be unique across all of the
   * components in an app.
   */
  id: PropTypes.string,

  /**
   * The children of this component
   */
  children: PropTypes.node,

  /**
   * Defines CSS styles which will override styles previously set.
   */
  style: PropTypes.object,

  /**
   * Often used with CSS to style elements with common properties.
   */
  className: PropTypes.string,

  /**
   * The id of the element to attach the tooltip to
   */
  target: PropTypes.string,

  /**
   * boundaries for popper, can be scrollParent, window, viewport, or any DOM element
   */
  boundariesElement: PropTypes.string,

  /**
   * Hide arrow on tooltip
   */
  hideArrow: PropTypes.bool,

  /**
   * Where to inject the popper DOM node, default body
   */
  container: PropTypes.string,

  /**
   * optionally override show/hide delays - default { show: 0, hide: 250 }
   */
  delay: PropTypes.oneOfType([
    PropTypes.shape({show: PropTypes.number, hide: PropTypes.number}),
    PropTypes.number
  ]),

  /**
   * CSS classes to apply to the inner-tooltip
   */
  innerClassName: PropTypes.string,

  /**
   * CSS classes to apply to the arrow-tooltip ('arrow' by default)
   */
  arrowClassName: PropTypes.string,

  /**
   * Optionally hide tooltip when hovering over tooltip content - default true
   */
  autohide: PropTypes.bool,

  /**
   * How to place the tooltip.
   */
  placement: PropTypes.oneOf([
    'auto',
    'auto-start',
    'auto-end',
    'top',
    'top-start',
    'top-end',
    'right',
    'right-start',
    'right-end',
    'bottom',
    'bottom-start',
    'bottom-end',
    'left',
    'left-start',
    'left-end'
  ]),

  /**
   * Tooltip offset
   */
  offset: PropTypes.oneOfType([PropTypes.string, PropTypes.number])
};

export default Tooltip;