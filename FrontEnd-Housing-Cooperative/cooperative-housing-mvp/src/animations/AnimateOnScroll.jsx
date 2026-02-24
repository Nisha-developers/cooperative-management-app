import { motion } from "framer-motion";

// ─── Base variants ───────────────────────────────────────────────

export const fadeUp = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -30 },
};

export const fadeDown = {
  hidden: { opacity: 0, y: -40 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 30 },
};

export const fadeLeft = {
  hidden: { opacity: 0, x: -60 },
  visible: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 60 },
};

export const fadeRight = {
  hidden: { opacity: 0, x: 20 },
  visible: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -20 },
};

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.85 },
  visible: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.9 },
};

export const slideUp = {
  hidden: { opacity: 0, y: 80 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -60 },
};

// ─── Stagger container ───────────────────────────────────────────

export const staggerContainer = (staggerChildren = 0.12, delayChildren = 0.1) => ({
  hidden: {},
  visible: {
    transition: {
      staggerChildren,
      delayChildren,
    },
  },
});

// ─── AnimateOnScroll wrapper ─────────────────────────────────────
// Use this to wrap any element and animate it when it enters the viewport

export const AnimateOnScroll = ({
  children,
  variant = fadeUp,
  delay = 0,
  duration = 0.6,
  className = "",
  once = true,
  amount = 0.15,
}) => {
  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      exit="exit"
      viewport={{ once, amount }}
      variants={variant}
      transition={{
        duration,
        delay,
        ease: [0.22, 1, 0.36, 1],
      }}
    >
      {children}
    </motion.div>
  );
};

// ─── Stagger wrapper — wraps a list of items ─────────────────────
// Children must use AnimateOnScroll or motion elements with variants

export const StaggerWrapper = ({
  children,
  className = "",
  stagger = 0.12,
  delay = 0.1,
  once = true,
  amount = 0.1,
}) => {
  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      exit="exit"
      viewport={{ once, amount }}
      variants={staggerContainer(stagger, delay)}
    >
      {children}
    </motion.div>
  );
};

// ─── StaggerItem — use inside StaggerWrapper ─────────────────────

export const StaggerItem = ({
  children,
  variant = fadeUp,
  duration = 0.6,
  className = "",
}) => {
  return (
    <motion.div
      className={className}
      variants={variant}
      transition={{
        duration,
        ease: [0.22, 1, 0.36, 1],
      }}
    >
      {children}
    </motion.div>
  );
};

// ─── AnimatedText — animates heading word by word ────────────────

export const AnimatedText = ({ text, className = "", delay = 0 }) => {
  const words = text.split(" ");
  return (
    <motion.span
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.5 }}
      variants={staggerContainer(0.08, delay)}
    >
      {words.map((word, i) => (
        <motion.span
          key={i}
          className="inline-block mr-[0.25em]"
          variants={fadeUp}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          {word}
        </motion.span>
      ))}
    </motion.span>
  );
};

export default AnimateOnScroll;